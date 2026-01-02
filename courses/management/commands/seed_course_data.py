from __future__ import annotations

import re
from datetime import time
from pathlib import Path

from django.core.management.base import BaseCommand

from courses.models import Course


class Command(BaseCommand):
    help = "Seed the database with Course 1 data from course_1_syllabus.md"

    def handle(self, *args, **options):
        syllabus_path = Path(__file__).resolve().parents[3] / "course_1_syllabus.md"
        if not syllabus_path.exists():
            self.stderr.write("course_1_syllabus.md not found in project root.")
            return

        content = syllabus_path.read_text(encoding="utf-8")

        title = _extract_title(content)
        description = _clean_markdown_noise(_extract_section(content, "Course Description"))
        what_youll_learn = _extract_bullets(content, "What Students Will Learn")
        syllabus = _clean_syllabus_markdown(_extract_section(content, "Course Outline"))
        instructor_name = _extract_instructor_name(content)
        instructor_bio = _build_instructor_bio(content)

        short_description = _first_sentence(description)
        long_description = description.strip()

        course, created = Course.objects.update_or_create(
            slug="build-a-web-application",
            defaults={
                "title": f"Course 1: {title}",
                "short_description": short_description,
                "long_description": long_description,
                "what_youll_learn": "\n".join(what_youll_learn),
                "syllabus": syllabus,
                "location": "ICS — Thursday Homeschool Learning Group",
                "day_of_week": Course.DayOfWeek.THURSDAY,
                "start_time": time(12, 0),
                "session_length_minutes": 60,
                "max_students": None,
                "published": True,
                "image_path": "images/courses/course-1-build-web-app.png",
                "instructor_name": instructor_name,
                "instructor_bio": instructor_bio,
            },
        )

        action = "Created" if created else "Updated"
        self.stdout.write(f"{action} course: {course.title}")


def _extract_title(content: str) -> str:
    match = re.search(r"## Course Title\s+\*\*(.+?)\*\*", content, re.S)
    if match:
        return match.group(1).strip()
    return "Build a Web Application"


def _extract_section(content: str, heading: str) -> str:
    pattern = rf"## {re.escape(heading)}\s+(.*?)(?:\n## |\Z)"
    match = re.search(pattern, content, re.S)
    if not match:
        return ""
    return match.group(1).strip()


def _extract_bullets(content: str, heading: str) -> list[str]:
    section = _extract_section(content, heading)
    bullets = re.findall(r"^- (.+)", section, re.M)
    return [item.strip() for item in bullets]


def _first_sentence(text: str) -> str:
    if not text:
        return ""
    sentence = text.split(".")[0].strip()
    if sentence and not sentence.endswith("."):
        sentence += "."
    return sentence


def _clean_markdown_noise(text: str) -> str:
    if not text:
        return ""
    cleaned_lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.strip("-").strip() == "":
            continue
        cleaned_lines.append(line)
    return "\n".join(cleaned_lines).strip()


def _clean_syllabus_markdown(text: str) -> str:
    if not text:
        return ""
    cleaned_lines = []
    previous_blank = False
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.strip("-").strip() == "":
            if not previous_blank:
                cleaned_lines.append("")
                previous_blank = True
            continue
        normalized = re.sub(r"^#{2,6}\s+", "", stripped)
        normalized = normalized.replace("**", "")
        cleaned_lines.append(normalized)
        previous_blank = False
    return "\n".join(cleaned_lines).strip()


def _extract_instructor_name(content: str) -> str:
    match = re.search(r"## Instructor\s+\*\*(.+?)\*\*", content, re.S)
    if match:
        return match.group(1).strip()
    return ""


def _build_instructor_bio(content: str) -> str:
    role = _extract_section(content, "Instructor Role (Volunteer)")
    credentials = _extract_section(content, "Instructor Credentials")
    parts = []
    if role:
        parts.append(role.strip())
    if credentials:
        parts.append(credentials.strip())
    return "\n\n".join(parts)
