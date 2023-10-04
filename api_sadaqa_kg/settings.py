import os.path
from pathlib import Path

import stripe

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-y&*(0y=!)%x1n5=*mkhsb2ozj#fdxeiwq&i-s3om5ab#z97*$x'

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'documents.apps.DocumentsConfig',
    'catalogs.apps.CatalogsConfig',
    'rest_framework',
    'djstripe'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'api_sadaqa_kg.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'api_sadaqa_kg.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
# STATIC_ROOT = BASE_DIR / "static"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

stripe.api_key = "sk_test_51NtvDNBVnhNGgAF1YPjzNqxhHpUb4es5y6m9byyB1qoOTLw9aSD3ERGHvxGqzT6RBET15GgNVqFS4mIjPrWMloT0000G1IobS6"

# Payment
STRIPE_LIVE_SECRET_KEY = os.environ.get("STRIPE_LIVE_SECRET_KEY",
                                        "sk_test_51NtvDNBVnhNGgAF1YPjzNqxhHpUb4es5y6m9byyB1qoOTLw9aSD3ERGHvxGqzT6RBET15GgNVqFS4mIjPrWMloT0000G1IobS6")
STRIPE_TEST_SECRET_KEY = os.environ.get("STRIPE_TEST_SECRET_KEY",
                                        "sk_test_51NtvDNBVnhNGgAF1YPjzNqxhHpUb4es5y6m9byyB1qoOTLw9aSD3ERGHvxGqzT6RBET15GgNVqFS4mIjPrWMloT0000G1IobS6")
STRIPE_LIVE_MODE = False  # Change to True in production
DJSTRIPE_WEBHOOK_SECRET = "whsec_7bbe630d063547bebf49667d52c896a3845482971b04e4a6bdea891d6b7b818b"  # Get it from the section in the Stripe dashboard where you added the webhook endpoint
DJSTRIPE_USE_NATIVE_JSONFIELD = True  # We recommend setting to True for new installations
DJSTRIPE_FOREIGN_KEY_TO_FIELD = "id"
