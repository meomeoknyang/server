"""
Django settings for meomeoknyang project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from datetime import timedelta
from pathlib import Path
import json, logging
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_FILE_STORAGE = 'config.asset_storage.MediaStorage'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

import os
from django.core.exceptions import ImproperlyConfigured 

def get_env_variable(var_name):
  try:
    return os.environ[var_name]
  except KeyError:
    error_msg = 'Set the {} environment variable'.format(var_name)
    raise ImproperlyConfigured(error_msg)

SECRET_KEY= get_env_variable('DJANGO_SECRET')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# CustomLogglyFormatter 클래스 정의
class CustomLogglyFormatter(logging.Formatter):
    def format(self, record):
        try:
            # format 문자열을 직접 구성
            formatted_message = f'[MeomeoKnyang] {record.levelname} {self.formatTime(record)} {record.getMessage()}'
            
            loggly_data = {
                'message': formatted_message,
                'level': record.levelname,
                'timestamp': self.formatTime(record),
            }
            return json.dumps(loggly_data)
        except Exception as e:
            return f"Logging format error: {str(e)}"


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[MeomeoKnyang] %(levelname)s %(asctime)s %(message)s',
        },
    },
    'handlers': {
        'loggly': {
            'level': 'INFO',
            'class': 'logging.handlers.HTTPHandler',
            'host': 'logs-01.loggly.com',
            'url': '/inputs/f1aa5f13-e707-49af-a993-e7a53be9ce6b/tag/http/',
            'method': 'POST',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['loggly', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'meomeoknyang': {
            'handlers': ['loggly', 'console'],
            'level': 'INFO',
            'propagate': True,
        }
    },
}

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    'storages',
    "django.contrib.staticfiles",
    "rest_framework",
    "restaurants",
    "django_filters",
    "reviews",
    "users",
    "baseplace",
    "cafe",
    "stamps",
    "drf_yasg",
    "search",
    'corsheaders',
]


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),  # 토큰 유효기간 설정
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
}

AUTH_USER_MODEL = 'users.CustomUser'

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = "meomeoknyang.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "meomeoknyang.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()
# SECRET_KEY = os.getenv('DJANGO_SECRET')
DATABASES = {
    'default': {
        # 'ENGINE': os.getenv('DB_ENGINE'),
        # 'NAME': os.getenv('DB_NAME'),
        # 'USER': os.getenv('DB_USER'),
        # 'PASSWORD': os.getenv('DB_PASSWORD'),
        # 'HOST': os.getenv('DB_HOST'),
        # 'PORT': os.getenv('DB_PORT'),
        'ENGINE': 'django.db.backends.postgresql',
		'NAME': get_env_variable('DB_NAME'),
        'USER': get_env_variable('DB_USER'),
        'PASSWORD': get_env_variable('DB_PASSWORD'),
        'HOST': get_env_variable('DB_HOST'),
        'PORT': get_env_variable('DB_PORT'),
    }
}

# S3로 미디어 파일 관리

# AWS_S3_CUSTOM_DOMAIN = os.getenv('AWS_CLOUDFRONT_DOMAIN')
AWS_S3_CUSTOM_DOMAIN = get_env_variable('AWS_CLOUDFRONT_DOMAIN')

STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'   

# 업로드된 미디어 파일의 URL
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
MEDIA_ROOT = None 

# AWS S3 설정
# AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
# AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')

AWS_ACCESS_KEY_ID = get_env_variable('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = get_env_variable('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = get_env_variable('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = get_env_variable('AWS_S3_REGION_NAME')




# # S3 업로드 관련 설정
# AWS_S3_OBJECT_PARAMETERS = {
#     'CacheControl': 'max-age=86400',  # 캐싱 정책 설정 (24시간)
# }

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
