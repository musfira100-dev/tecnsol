"""
Django settings for the Tecnsol project.
"""
from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from a .env file sitting next to manage.py.
# This file is listed in .gitignore, so your real credentials never get
# committed or shared — see the note near EMAIL_HOST_USER below.
load_dotenv(BASE_DIR / '.env')

# Set DJANGO_SECRET_KEY as an environment variable on Render.
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-change-this-secret-key-before-deploying-!!!'
)

# Defaults to False for safety. For local work, add DJANGO_DEBUG=True to your .env
DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.environ.get(
    'DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1'
).split(',')

CSRF_TRUSTED_ORIGINS = [
    o for o in os.environ.get('DJANGO_CSRF_TRUSTED_ORIGINS', '').split(',') if o
]

# Cloudinary only switches on when CLOUDINARY_URL is set (i.e. on Render)
USE_CLOUDINARY = bool(os.environ.get('CLOUDINARY_URL'))

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
]
if USE_CLOUDINARY:
    INSTALLED_APPS.append('cloudinary_storage')   # must come before staticfiles
INSTALLED_APPS.append('django.contrib.staticfiles')
if USE_CLOUDINARY:
    INSTALLED_APPS.append('cloudinary')

# Local apps
INSTALLED_APPS.append('core')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tecnsol.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.site_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'tecnsol.wsgi.application'
ASGI_APPLICATION = 'tecnsol.asgi.application'

# Database
# SQLite locally; PostgreSQL on Render (read from the DATABASE_URL variable).
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600,
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'core' / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files (images uploaded through the admin panel)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STORAGES = {
    "default": {
        "BACKEND": (
            "cloudinary_storage.storage.MediaCloudinaryStorage"
            if USE_CLOUDINARY
            else "django.core.files.storage.FileSystemStorage"
        ),
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

# Render sits behind a proxy that terminates HTTPS
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --------------------------------------------------------------------------
# Contact / Apply Now form email notifications
# --------------------------------------------------------------------------
# Real credentials live in a `.env` file next to manage.py locally (never in
# this file, and never committed to git), and in Render's Environment tab
# when deployed:
#
#   DJANGO_EMAIL_HOST_USER=youraddress@gmail.com
#   DJANGO_EMAIL_HOST_PASSWORD=your-16-char-gmail-app-password
#   DJANGO_NOTIFY_EMAIL=whereyouwantinquiries@gmail.com   (optional — defaults
#                                                           to the Contact
#                                                           Email set in
#                                                           Site Settings)
EMAIL_HOST_USER = os.environ.get('DJANGO_EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('DJANGO_EMAIL_HOST_PASSWORD', '')

if EMAIL_HOST_USER and EMAIL_HOST_PASSWORD:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.environ.get('DJANGO_EMAIL_HOST', 'smtp.gmail.com')
    EMAIL_PORT = int(os.environ.get('DJANGO_EMAIL_PORT', '587'))
    EMAIL_USE_TLS = os.environ.get('DJANGO_EMAIL_USE_TLS', 'True') == 'True'
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
else:
    # No SMTP credentials found — inquiries still save to the database and
    # show up in the admin panel, but the email just prints to the terminal.
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    DEFAULT_FROM_EMAIL = 'no-reply@tecnsol.io'

# Inbox that receives every Contact / Apply Now submission. Falls back to
# the Contact Email field in Site Settings (admin panel) when unset.
NOTIFY_EMAIL = os.environ.get('DJANGO_NOTIFY_EMAIL', '')