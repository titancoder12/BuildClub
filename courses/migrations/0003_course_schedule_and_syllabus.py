from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0002_course_instructor_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="syllabus",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="course",
            name="start_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="course",
            name="end_date",
            field=models.DateField(blank=True, null=True),
        ),
    ]
