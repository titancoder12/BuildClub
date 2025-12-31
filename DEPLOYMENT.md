# Deployment (Ubuntu)

This guide outlines a straightforward deployment using Gunicorn, Nginx, and systemd.

## 1) System packages
```bash
sudo apt update
sudo apt install python3-venv python3-pip nginx
```

## 2) Create a deploy user and app directory
```bash
sudo adduser buildclub
sudo mkdir -p /srv/buildclub
sudo chown -R buildclub:buildclub /srv/buildclub
```

## 3) Install the app
```bash
sudo -u buildclub git clone <your-repo-url> /srv/buildclub/app
cd /srv/buildclub/app
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_course_data
python manage.py collectstatic --noinput
```

## 4) Environment variables
Set these in your systemd service file or a secure environment file:
- `DJANGO_SETTINGS_MODULE=buildclub_site.settings`
- `SECRET_KEY=<your-secret-key>`
- `DEBUG=False`
- `ALLOWED_HOSTS=<your-domain>`

## 5) Gunicorn systemd service
Create `/etc/systemd/system/buildclub.service`:
```ini
[Unit]
Description=Build Club Django App
After=network.target

[Service]
User=buildclub
Group=www-data
WorkingDirectory=/srv/buildclub/app
Environment="DJANGO_SETTINGS_MODULE=buildclub_site.settings"
Environment="SECRET_KEY=<your-secret-key>"
Environment="DEBUG=False"
Environment="ALLOWED_HOSTS=<your-domain>"
ExecStart=/srv/buildclub/app/.venv/bin/gunicorn buildclub_site.wsgi:application --bind 127.0.0.1:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now buildclub
```

## 6) Nginx configuration
Create `/etc/nginx/sites-available/buildclub`:
```nginx
server {
    listen 80;
    server_name <your-domain>;

    location /static/ {
        alias /srv/buildclub/app/staticfiles/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/buildclub /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Static files
- `collectstatic` writes into the `staticfiles/` directory.
- Update the Nginx static alias if you change `STATIC_ROOT`.

## Database considerations
- SQLite is suitable for development and small deployments.
- For larger usage, switch to PostgreSQL and update `DATABASES` in `buildclub_site/settings.py`.

## Security notes
- Always set `DEBUG=False` in production.
- Set a strong `SECRET_KEY`.
- Configure `ALLOWED_HOSTS` for your domain.
- Consider HTTPS with Let’s Encrypt for production traffic.
