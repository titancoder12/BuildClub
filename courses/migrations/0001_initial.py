from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("slug", models.SlugField(max_length=200, unique=True)),
                ("short_description", models.CharField(max_length=300)),
                ("long_description", models.TextField()),
                ("what_youll_learn", models.TextField()),
                ("location", models.CharField(max_length=200)),
                ("day_of_week", models.CharField(choices=[("Monday", "Monday"), ("Tuesday", "Tuesday"), ("Wednesday", "Wednesday"), ("Thursday", "Thursday"), ("Friday", "Friday"), ("Saturday", "Saturday"), ("Sunday", "Sunday")], max_length=12)),
                ("start_time", models.TimeField()),
                ("session_length_minutes", models.PositiveIntegerField()),
                ("max_students", models.PositiveIntegerField(blank=True, null=True)),
                ("published", models.BooleanField(default=False)),
                ("image_path", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["created_at"],
            },
        ),
        migrations.CreateModel(
            name="Registration",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("student_first_name", models.CharField(max_length=100)),
                ("student_last_name", models.CharField(max_length=100)),
                ("student_grade", models.CharField(max_length=50)),
                ("guardian_name", models.CharField(max_length=200)),
                ("guardian_email", models.EmailField(max_length=254)),
                ("notes", models.TextField(blank=True)),
                ("consent", models.BooleanField(default=False)),
                ("status", models.CharField(choices=[("Pending", "Pending"), ("Confirmed", "Confirmed"), ("Waitlisted", "Waitlisted"), ("Cancelled", "Cancelled")], default="Pending", max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("course", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="registrations", to="courses.course")),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]
