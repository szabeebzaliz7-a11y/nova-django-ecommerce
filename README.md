# NOVA — Django E-commerce Technical Assignment

A custom Apple-inspired e-commerce experience built with Python and Django.

## Apps
- `store`: customer-facing website, products, categories, banners, authentication and session bag.
- `dashboard`: custom staff-only management dashboard for products, categories and banners.
- Django's built-in `/django-admin/` is also enabled.

## Requirements covered
- Dynamic homepage banners
- Product/category CRUD
- Product detail pages
- User registration/login/logout
- Protected account page
- Responsive frontend
- Staff dashboard
- Django Admin
- SQLite database
- Image uploads
- Search/filtering
- Session-based demo shopping bag

## Setup

```bash
python -m venv venv
venv\\Scripts\\activate       # Windows
pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open:
- Store: http://127.0.0.1:8000/
- Custom dashboard: http://127.0.0.1:8000/dashboard/
- Django admin: http://127.0.0.1:8000/django-admin/

Login with the superuser to access the dashboard.

## Add demo data
Use the dashboard to create categories, products and banners. Upload your own royalty-free images.

## Deployment on Render
Build command:
`pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`

Start command:
`gunicorn apple_store.wsgi:application`

Set:
- `DJANGO_SECRET_KEY`
- `DEBUG=False`
- `CSRF_TRUSTED_ORIGINS=https://your-app.onrender.com`

For production, move media uploads to S3/Cloudinary because Render's local filesystem is not persistent.

## Submission
Mention:
- Python + Django
- HTML/CSS/JavaScript
- SQLite
- Pillow
- WhiteNoise
- Gunicorn
- Custom dashboard
- Django authentication
- Session-based demo bag

The visual style is original and only uses an Apple Store concept as inspiration. Do not use Apple's copyrighted assets or source code.
