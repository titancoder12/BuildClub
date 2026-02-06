from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0003_course_schedule_and_syllabus"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="instructor_cv_markdown",
            field=models.TextField(
                blank=True,
                default="",
                help_text="Paste the instructor CV in Markdown format.",
            ),
        ),
    ]
