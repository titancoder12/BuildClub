# Build Club Website

## Project overview
Build Club is a student-led initiative focused on teaching students how to build technology from the ground up. The program emphasizes hands-on construction, problem-solving, and systems thinking across software and hardware, including microcontrollers, processors, and 3D printing. Students build real, professional-looking projects while learning how systems work before relying on automation tools.

## Tech stack
- Django (templates, admin, ORM)
- Tailwind CSS via CDN
- SQLite for development

## Features
- Home page with program overview and learning focus areas
- Courses index with published courses only
- Course detail pages with syllabus-driven learning outcomes
- Registration flow with capacity enforcement
- Django admin for managing courses and registrations
- CSV export for registrations

## Screens/pages
- `/` Home page
- `/courses/` Courses list
- `/courses/<slug>/` Course detail
- `/courses/<slug>/register/` Registration form
- `/register/success/` Registration success
- `/admin/` Admin dashboard

## Run locally
1. Create and activate a virtual environment.
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Seed Course 1: `python manage.py seed_course_data`
5. Start the server: `python manage.py runserver`

## Django admin access
1. Create a superuser: `python manage.py createsuperuser`
2. Visit `http://127.0.0.1:8000/admin/` and log in.

## Add or edit courses
- Go to the Courses section in Django admin.
- Set `published = true` to show a course on the public site.
- Add location, day of week, start time, session length, and capacity.

## View or export registrations
- Go to Registrations in Django admin.
- Select registrations and choose the “Export selected registrations as CSV” action.

## Documentation
- `LOCAL_SETUP.md` for environment setup and troubleshooting
- `DEPLOYMENT.md` for production deployment guidance
- `ADMIN_GUIDE.md` for non-technical admin usage
