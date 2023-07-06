"""
Django settings for Technical project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from datetime import timedelta
from pathlib import Path
import logging.config
from django.conf import settings
from dotenv import load_dotenv
import dj_database_url
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# cloudnary
import cloudinary


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# Set the project base directory
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG')
# DEBUG=True
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')


ALLOWED_HOSTS = ['localhost','127.0.0.1',]


# Application definition

INSTALLED_APPS = [
    # "daphne",
     "whitenoise.runserver_nostatic",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    'django.contrib.humanize',
    # created
    "Job",
    "Application",
    "Account",
    "Page",
    # installed
    # 'django-environ',
    'cloudinary',
    "debug_toolbar",
    "django_social_share",
    "ckeditor",
    "taggit",
    'storages',
    "django_daraja",
    "django_celery_results",
    "crispy_forms",
    "crispy_bootstrap5",
    "django_browser_reload",
    "django_filters",
    "phonenumber_field",
    'hitcount',
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    # providers
    "allauth.socialaccount.providers.google",
    "channels",
]
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]
INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]
ROOT_URLCONF = "Technical.urls"
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            # "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "KEY_PREFIX": "Technical",
        "TIMEOUT": 86400,
    }
}
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR.joinpath("templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "Technical.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# development db settings
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": os.getenv("NAME"),
#         "USER": os.getenv("USER"),
#         "PASSWORD": os.getenv("PASSWORD"),
#         "HOST": os.getenv("HOST"),
#         "PORT": os.getenv("PORT"),
#     }
# }
# production db settings
DATABASE_URL = os.getenv("DATABASE_URL")
DATABASES = {
    "default": dj_database_url.config(
        conn_max_age=600,
        conn_health_checks=True,
    )
}
# EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = "smtp.sendgrid.net"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
# SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
RECIPIENT_ADDRESS = os.getenv("RECIPIENT_ADDRESS")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL",)
# twilio
TWILIO_ACCOUNT_SID = os.getenv("account_sid")
TWILIO_AUTH_TOKEN = os.getenv("auth_token")

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    # },
    # {
    #     "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    # },
    # {
    #     "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    # },
    # {
    #     "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    # },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR / "staticfiles")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

# media
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR / "media")
CKEDITOR_UPLOAD_PATH = "content/ckeditor/"
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# asgi
ASGI_APPLICATION = "Technical.asgi.application"
CHANNEL_LAYERS = {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}


SITE_ID = 2
LOGIN_REDIRECT_URL = "jobs"
LOGOUT_REDIRECT_URL = "jobs"


# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
ACCOUNT_SESSION_REMEMBER = None


# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        "APP": {
            "client_id": os.getenv("client_id"),
            "secret": os.getenv("secret"),
            "key": "",
        }
    }
}
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = settings.LOGIN_URL
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = None
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
# ACCOUNT_EMAIL_CONFIRMATION_HMAC = True
ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_EMAIL_VERIFICATION = "mandatory"
# ACCOUNT_EMAIL_CONFIRMATION_COOLDOWN =180
ACCOUNT_EMAIL_MAX_LENGT = 254
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300
# ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = False
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = False
ACCOUNT_LOGIN_ON_PASSWORD_RESET = False
ACCOUNT_LOGOUT_REDIRECT_URL = settings.LOGOUT_REDIRECT_URL
ACCOUNT_PREVENT_ENUMERATION = True
ACCOUNT_RATE_LIMITS = {
    # Change password view (for users already logged in
    "change_password": "5/m",
    # Email management (e.g. add, remove, change primary
    "manage_email": "10/m",
    # Request a password reset, global rate limit per IP
    "reset_password": "20/m",
    # Rate limit measured per individual email address
    "reset_password_email": "5/m",
    # Password reset (the view the password reset email links to.
    "reset_password_from_key": "20/m",
    # Signups.
    "signup": "20/m",
    # NOTE: Login is already protected via `ACCOUNT_LOGIN_ATTEMPTS_LIMIT`
}
ACCOUNT_SESSION_REMEMBER = None
# ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
ACCOUNT_SIGNUP_REDIRECT_URL = settings.LOGIN_REDIRECT_URL
ACCOUNT_USERNAME_BLACKLIST = ["admin"]
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_MIN_LENGTH = 5
ACCOUNT_USERNAME_REQUIRED = True
# SOCIALACCOUNT_LOGIN_ON_GET =True

# phonenumber_field
PHONENUMBER_DEFAULT_REGION = "KE"
# celery redis
CELERY_BROKER_URL = "redis://localhost:6379"
# CELERY_ACCEPT_CONTENT =['json']
# CELERY_TASK_SERIALIZER = ['json']

# CELERY_RESULT_BACKEND = "redis://localhost:6379"
# Specify the default queue name for Celery
CELERY_DEFAULT_QUEUE = "default"
# Specify additional Celery configuration (optional)
CELERY_CONFIG = {
    "worker_prefetch_multiplier": 1,
    "task_acks_late": True,
}
# Set the Celery beat schedule
CELERY_BEAT_SCHEDULE = {
    "update_job_status": {
        "task": "Job.tasks.update_job_expiry_status",
        "schedule": timedelta(minutes=15),  # Run every 15 minutes
    },
}
CELERY_RESULT_BACKEND = "django-db"
CELERY_CACHE_BACKEND = "default"

# django setting.
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
#         'LOCATION': 'my_cache_table',
#     }
# }
# mpesa

# MPESA_CONFIG = {
# ‘CONSUMER_KEY’: ‘<Your consumer key from daraja>’,
# ‘CONSUMER_SECRET’: ‘<Your consumer secret from daraja>’,
# ‘HOST_NAME’: ‘<Your hostname e.g https://myhostname>’,
# ‘PASS_KEY’: ‘<Your pass key from daraja>’,
# ‘SAFARICOM_API’: ‘https://sandbox.safaricom.co.ke’,
# ‘SHORT_CODE’: ‘174379’

# }
# The Mpesa environment to use
# Possible values: sandbox, production

MPESA_ENVIRONMENT = "sandbox"

# Credentials for the daraja app

MPESA_CONSUMER_KEY = os.getenv("MPESA_CONSUMER_KEY")
MPESA_CONSUMER_SECRET = os.getenv("MPESA_CONSUMER_SECRET")

# Shortcode to use for transactions. For sandbox  use the Shortcode 1 provided on test credentials page

MPESA_SHORTCODE = "174379"

# Shortcode to use for Lipa na MPESA Online (MPESA Express) transactions
# This is only used on sandbox, do not set this variable in production
# For sandbox use the Lipa na MPESA Online Shorcode provided on test credentials page

MPESA_EXPRESS_SHORTCODE = "174379"

# Type of shortcode
# Possible values:
# - paybill (For Paybill)
# - till_number (For Buy Goods Till Number)

MPESA_SHORTCODE_TYPE = "paybill"

# Lipa na MPESA Online passkey
# Sandbox passkey is available on test credentials page
# Production passkey is sent via email once you go live

MPESA_PASSKEY = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"

# Username for initiator (to be used in B2C, B2B, AccountBalance and TransactionStatusQuery Transactions)

MPESA_INITIATOR_USERNAME = "testapi"

# Plaintext password for initiator (to be used in B2C, B2B, AccountBalance and TransactionStatusQuery Transactions)

MPESA_INITIATOR_SECURITY_CREDENTIAL = "Safaricom999!*!"

# hitcount
HITCOUNT_KEEP_HIT_ACTIVE = { 'days': 7 }

# ckeditor

CKEDITOR_CONFIGS = {
    "default": {
        'skin': 'moono',
        # 'skin': 'office2013',
        "toolbar_Basic": [["Source", "-", "Bold", "Italic"]],
         # 'filebrowserUploadUrl': '/your-file-upload-url/',
        # 'filebrowserUploadMethod': 'form',
        'filebrowserImageUploadAllowed': True,
        'filebrowserImageMaxSize': 5242880,  # 5MB in bytes
        "toolbar_YourCustomToolbarConfig": [
            {
                "name": "clipboard",
                "items": ["Cut", "Copy", "Paste", "-", "Undo", "Redo"],
            },
            {
                "name": "basicstyles",
                "items": [
                    "Bold",
                    "Italic",
                    "Underline",
                    "Subscript",
                    "Superscript",
                    "-",
                ],
            },
            {
                "name": "paragraph",
                "items": [
                    "NumberedList",
                    "BulletedList",
                    "-",
                    "Outdent",
                    "Indent",
                    "-",
                    "Blockquote",
                    "JustifyLeft",
                    "JustifyCenter",
                    "JustifyRight",
                    "JustifyBlock",
                    "-",
                ],
            },
            {
                "name": "insert",
                "items": ["Table", "HorizontalRule", "SpecialChar"],
            },
           
            "/",
            {"name": "styles", "items": ["Styles", "Format", "Font", "FontSize"]},
            {"name": "colors", "items": ["TextColor", "BGColor"]},
            {"name": "tools", "items": ["Maximize"]},
        ],
        "toolbar": "YourCustomToolbarConfig",  # put selected toolbar config here
        # 'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
        "height": 291,
        "width": "auto",
        # 'filebrowserWindowHeight': 725,
        # 'filebrowserWindowWidth': 940,
        # 'toolbarCanCollapse': True,
        # 'mathJaxLib': '//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML',
        "tabSpaces": 4,
        "removeDialogTabs": "link:advanced;link:upload;link:target;image:advanced;image:Link",
        "extraPlugins": ",".join(
            [
                "uploadimage",  # the upload image feature
                # your extra plugins here
                "div",
                "autolink",
                "autoembed",
                "embedsemantic",
                "autogrow",
                # 'devtools',
                "widget",
                "lineutils",
                "clipboard",
                "dialog",
                "dialogui",
                "elementspath",
            ]
        ),
    },
    'non_main':{
        'toolbar': 'Custom',
        'skin': 'moono',
         "height": 291,
        "width": "auto",
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
           
           
        ]
    },
}

# cloudinary

cloudinary.config( 
  cloud_name = os.getenv("cloud_name"), 
  api_key = os.getenv("api_key"), 
  api_secret = os.getenv("api_secret"),
  secure = True
)
import cloudinary.uploader
import cloudinary.api


LOGGING_CONFIG =None
LOGGING ={
    "version" : 1,
    "disable_existing_loggers":False,
    "formatters":{
        "verbose":{
            "()":"colorlog.ColoredFormatter",
            "format":"%(log_color)s %(levelname)-8s %(asctime)s %(request_id)s %(process)s %(filename)s %(lineno)-8s [%(name)s] %(funcName)-24s : %(message)s",
            "log_colors":{
                "DEBUG":"blue",
                "INFO":"white",
                "ERROR":"red",
                "WARNING":"yellow"
            },

            
        },
        "simple":{
            "format": "%(levelname)s %(asctime)s %(name)s %(module)s %(filename)s %(lineno)d %(funcName)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "filters":{
        "request_id" : {"()": "log_request_id.filters.RequestIDFilter"},
        
    },
    "handlers":{
        "console":{
            "class":"logging.StreamHandler",
            "formatter":"verbose",
            "filters":["request_id"]
        },
        "sentry":{
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
    },
    "loggers":{
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
        "django.server":{
            'handlers':["console","sentry"],
            "level":"DEBUG",
            'propagate': False,
        },
    }
        
    },
DEBUG_PROPAGATE_EXCEPTIONS = True

COMPRESS_ENABLED = os.getenv('COMPRESS_ENABLED', False)



sentry_sdk.init(
    dsn="https://1ff2e206a6434010802660bac1bdb13c@o4504099387342848.ingest.sentry.io/4505467134607360",
    integrations=[
        DjangoIntegration(
            transaction_style="url",
            middleware_spans=True,
            signals_spans=False,
            ),
    ],

  
    traces_sample_rate=1.0,   
    send_default_pii=True
)

# aws settings

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
AWS_DEFAULT_ACL = "public-read"
# AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
# AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
AWS_QUERYSTRING_AUTH = False
AWS_QUERYSTRING_EXPIRE= 8
# AWS_S3_OBJECT_PARAMETERS = {"Access-Control-Allow-Origin": "*"}

# AWS_S3_CUSTOM_DOMAIN = 'https://d2n7j1cvfar59p.cloudfront.net'
# AWS_CLOUDFRONT_KEY = os.getenv("AWS_CLOUDFRONT_KEY",None).encode('ascii')
# AWS_CLOUDFRONT_KEY_ID =os.getenv("AWS_CLOUDFRONT_KEY_ID",None)
# s3 static settings
# AWS_LOCATION = "static"
# STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/"
# MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"

# boto3
# for media 
STORAGES = {
    "default": 
        {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage"
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
        }
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'
# for static files
# STORAGES = {"staticfiles": {"BACKEND": "storages.backends.s3boto3.S3StaticStorage"}}
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3ManifestStaticStorage'