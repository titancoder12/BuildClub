import csv

from django.contrib import admin
from django.http import HttpResponse

from .models import Course, Registration


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "published",
        "day_of_week",
        "start_time",
        "location",
        "instructor_name",
    )
    list_filter = ("published", "day_of_week")
    search_fields = ("title", "short_description", "long_description")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = (
        "student_first_name",
        "student_last_name",
        "course",
        "guardian_email",
        "status",
        "created_at",
    )
    list_filter = ("status", "course")
    search_fields = (
        "student_first_name",
        "student_last_name",
        "guardian_name",
        "guardian_email",
    )
    actions = ["export_as_csv"]

    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=registrations.csv"

        writer = csv.writer(response)
        writer.writerow(
            [
                "Course",
                "Student First Name",
                "Student Last Name",
                "Student Grade",
                "Guardian Name",
                "Guardian Email",
                "Notes",
                "Consent",
                "Status",
                "Created At",
            ]
        )
        for registration in queryset.select_related("course"):
            writer.writerow(
                [
                    registration.course.title,
                    registration.student_first_name,
                    registration.student_last_name,
                    registration.student_grade,
                    registration.guardian_name,
                    registration.guardian_email,
                    registration.notes,
                    "Yes" if registration.consent else "No",
                    registration.status,
                    registration.created_at.isoformat(),
                ]
            )
        return response

    export_as_csv.short_description = "Export selected registrations as CSV"
