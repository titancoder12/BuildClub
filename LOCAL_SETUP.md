# Local Setup

## Python version
- Python 3.11 or newer recommended.

## Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate
```

## Install dependencies
```bash
pip install -r requirements.txt
```

## Run migrations
```bash
python manage.py migrate
```

## Seed Course 1 data
```bash
python manage.py seed_course_data
```

## Start the development server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`.

## Common issues
- `ModuleNotFoundError: No module named 'django'`
  - Make sure your virtual environment is activated and dependencies are installed.
- `OperationalError: no such table`
  - Run migrations with `python manage.py migrate`.
- Images not loading
  - Confirm you are running the server from the project root and static files exist in `static/`.
