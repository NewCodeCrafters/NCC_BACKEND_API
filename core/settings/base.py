
from datetime import timedelta
from pathlib import Path
from decouple import config
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")


# Application definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

CUSTOM_USER = [
    "accounts",
    # 'teacher',
    'student',
]

THIRDPARTY_APPS = [
    "rest_framework",
    "djoser",
    'django_filters',
    "drf_yasg",
    'corsheaders',

]

INSTALLED_APPS = DJANGO_APPS + CUSTOM_USER + THIRDPARTY_APPS

AUTH_USER_MODEL = "accounts.User"

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Add this line
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

CORS_ALLOWED_ORIGINS = [
    "https://your-frontend-domain.com",
    "http://localhost:3000",  # For local development
    "http://127.0.0.1:3000",  # For local development
]

# CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = "core.urls"

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

WSGI_APPLICATION = "core.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}


# Djoser Configuration
DJOSER = {
    'SEND_ACTIVATION_EMAIL': False,  # Disable activation emails
    'SEND_CONFIRMATION_EMAIL': False,  # Disable confirmation emails
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': 'username/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': 'activate/{uid}/{token}',
    'USER_CREATE_PASSWORD_RETYPE': False,  # Disable password retype
    'SET_PASSWORD_RETYPE': False,  # Disable password retype
    'PASSWORD_RESET_CONFIRM_RETYPE': False,  # Disable password retype
    'LOGOUT_ON_PASSWORD_CHANGE': True,  # Logout after password change
    'PERMISSIONS': {
        'user_list': ['rest_framework.permissions.IsAdminUser'],  # Only admin can list users
        'user': ['rest_framework.permissions.IsAuthenticated'],  # Authenticated users can view their profile
    },
    'SERIALIZERS': {
        'user': 'accounts.serializers.CustomUserSerializer',  # Custom user serializer
        'current_user': 'accounts.serializers.CustomUserSerializer',  # Custom user serializer for current user
    },
    'HIDE_USERS': True,  # Hide user list from non-admin users
}

# Disable signup endpoint
DJOSER['ENDPOINTS'] = {
    'user': 'djoser.views.UserViewSet',
    'user_delete': 'djoser.views.UserViewSet',
    'user_me': 'djoser.views.UserViewSet',
    'token_create': 'djoser.views.TokenCreateView',  # Login
    'token_destroy': 'djoser.views.TokenDestroyView',  # Logout
}

