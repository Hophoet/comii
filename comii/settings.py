"""
Django settings for comii project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'yh_!j&ht$o5qmzct#kj+o2my*$nhia#$vyrcl7f=*7_^d$0^c!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'crispy_forms',

    'core',
    'stripetest'
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

ROOT_URLCONF = 'comii.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'comii.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
    #     'default': {
    #     'ENGINE': 'django.db.backends.postgresql', # on utilise l'adaptateur postgresql
    #     'NAME': 'comii', # le nom de notre base de donnees creee precedemment
    #     'USER': 'postgres', # attention : remplacez par votre nom d'utilisateur
    #     'PASSWORD': "Sxt7code'",
    #     'HOST': '',
    #     'PORT': '5432',
    # }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static_files')]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


AUTHENTICATION_BACKENDS = [
 # Needed to login by username in Django admin, regardless of `allauth`
 'django.contrib.auth.backends.ModelBackend',
 # `allauth` specific authentication methods, such as login by e-mail
 'allauth.account.auth_backends.AuthenticationBackend',
]


SITE_ID = 1
LOGIN_REDIRECT_URL = '/'

#CRISPY FORMS
CRISPY_TEMPLATE_PACK = 'bootstrap4'


#STRIPE 

STRIPE_PUBLISHABLE_KEY = 'pk_test_51HjXyDKvYCb6qstMpnORUwLDScnAXkO53G1IOPULIzbKkF7DOsxdDAC6I2LnNUj0YagJSFwAUXMES2N5oJEAY6se00XZAZdkcp'
STRIPE_SECRET_KEY = 'sk_test_51HjXyDKvYCb6qstMGs0Ou5ThGNHc5QUMCWeMoaEz2Po3agEQ2qbQUdhP6eNpPwYv1WCbcFnFrTwNaHtScv6FI8jl00Ay2xv9y4'

#EMAIL
EMAIL_HOST_USER='hophoet'
EMAIL_HOST_PASSWORD='fakePassword'

