import re

from django.db import models


class Course(models.Model):
    class DayOfWeek(models.TextChoices):
        MONDAY = "Monday", "Monday"
        TUESDAY = "Tuesday", "Tuesday"
        WEDNESDAY = "Wednesday", "Wednesday"
        THURSDAY = "Thursday", "Thursday"
        FRIDAY = "Friday", "Friday"
        SATURDAY = "Saturday", "Saturday"
        SUNDAY = "Sunday", "Sunday"

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    short_description = models.CharField(max_length=300)
    long_description = models.TextField()
    what_youll_learn = models.TextField()
    location = models.CharField(max_length=200)
    day_of_week = models.CharField(max_length=12, choices=DayOfWeek.choices)
    start_time = models.TimeField()
    session_length_minutes = models.PositiveIntegerField()
    max_students = models.PositiveIntegerField(null=True, blank=True)
    published = models.BooleanField(default=False)
    image_path = models.CharField(max_length=255)
    instructor_name = models.CharField(max_length=200, default="", blank=True)
    instructor_bio = models.TextField(default="", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self) -> str:
        return self.title

    def registered_count(self) -> int:
        return self.registrations.exclude(
            status=Registration.Status.CANCELLED
        ).count()

    def spots_remaining(self) -> int | None:
        if self.max_students is None:
            return None
        remaining = self.max_students - self.registered_count()
        return max(remaining, 0)

    def is_full(self) -> bool:
        if self.max_students is None:
            return False
        return self.registered_count() >= self.max_students

    def what_youll_learn_list(self) -> list[str]:
        return [item.strip() for item in self.what_youll_learn.splitlines() if item.strip()]

    def instructor_profile(self) -> dict[str, object]:
        if not (self.instructor_bio or self.instructor_name):
            return {}

        name = self.instructor_name.strip()
        role_intro = ""
        role_items: list[str] = []
        role_notes: list[str] = []
        credential_items: list[str] = []

        lines = [line.strip() for line in self.instructor_bio.splitlines()]
        section = "role"
        for line in lines:
            if not line:
                continue
            cleaned = _clean_instructor_line(line)
            if not cleaned or cleaned.strip("-").strip() == "":
                continue
            if cleaned.endswith("serves as:"):
                role_intro = cleaned
                section = "role"
                continue
            if cleaned == "Christopher Lin":
                if not name:
                    name = cleaned
                section = "credentials"
                continue
            if cleaned.startswith("- "):
                item = cleaned[2:].strip()
                if section == "role":
                    role_items.append(item)
                else:
                    credential_items.append(item)
                continue
            if section == "role":
                role_notes.append(cleaned)
            else:
                credential_items.append(cleaned)

        return {
            "name": name,
            "role_intro": role_intro,
            "role_items": role_items,
            "role_notes": role_notes,
            "credential_items": credential_items,
        }


class Registration(models.Model):
    class Status(models.TextChoices):
        PENDING = "Pending", "Pending"
        CONFIRMED = "Confirmed", "Confirmed"
        WAITLISTED = "Waitlisted", "Waitlisted"
        CANCELLED = "Cancelled", "Cancelled"

    course = models.ForeignKey(
        Course, related_name="registrations", on_delete=models.CASCADE
    )
    student_first_name = models.CharField(max_length=100)
    student_last_name = models.CharField(max_length=100)
    student_grade = models.CharField(max_length=50)
    guardian_name = models.CharField(max_length=200)
    guardian_email = models.EmailField()
    notes = models.TextField(blank=True)
    consent = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.student_first_name} {self.student_last_name} ({self.course})"


def _clean_instructor_line(text: str) -> str:
    cleaned = text.replace("**", "")
    cleaned = re.sub(r"\[(.+?)\]\((https?://[^\s)]+)\)", r"\1 (\2)", cleaned)
    return cleaned
