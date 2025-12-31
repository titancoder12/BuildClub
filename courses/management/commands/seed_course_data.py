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
        description = _extract_section(content, "Course Description")
        what_youll_learn = _extract_bullets(content, "What Students Will Learn")

        short_description = _first_sentence(description)
        long_description = description.strip()

        course, created = Course.objects.update_or_create(
            slug="build-a-web-application",
            defaults={
                "title": f"Course 1: {title}",
                "short_description": short_description,
                "long_description": long_description,
                "what_youll_learn": "\n".join(what_youll_learn),
                "location": "ICS — Thursday Homeschool Learning Group",
                "day_of_week": Course.DayOfWeek.THURSDAY,
                "start_time": time(12, 0),
                "session_length_minutes": 60,
                "max_students": None,
                "published": True,
                "image_path": "images/courses/course-1-build-web-app.png",
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
