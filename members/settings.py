import os
import ldap
from django_auth_ldap.config import LDAPSearch, PosixGroupType

from .localSettings import (LDAP_SERVER_URI, LDAP_AUTHENTICATION_DN,
LDAP_AUTHENTICATION_PASSWORD, LDAP_MANAGEMENT_DN, LDAP_MANAGEMENT_PASSWORD)

""" General project settings """

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-@2v3*j$uux!_lpbinu+e#9ro8a7-u34i&s0@c8^!f9b_77^g&'
DEBUG = True
ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'network.apps.NetworkConfig',
    'accounts.apps.AccountsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'compressor',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'members.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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

WSGI_APPLICATION = 'members.wsgi.application'

COMPRESS_PRECOMPILERS = (
    ('text/scss', 'bundle exec sass --scss {infile} {outfile}'),
)

STATICFILES_FINDERS = (
    'compressor.finders.CompressorFinder',
)

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(BASE_DIR, "static")
COMPRESS_ROOT = os.path.join(BASE_DIR, "static")
COMPRESS_ENABLED = True
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
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

# Authentication
AUTHENTICATION_BACKENDS = ['django_auth_ldap.backend.LDAPBackend',
                           'django.contrib.auth.backends.ModelBackend']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# TO DO : Remove hardcoded urls

LOGIN_URL = "/accounts/login/"

LOGIN_REDIRECT_URL = "/network/devices/"

# Internationalization
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

""" General informations """
PLATFORM_NAME = "members.atilla.org"
PLATFORM_HOSTNAME = "members.atilla.org"
PLATFORM_USING_HTTPS = False

""" LDAP Settings for LDAP authentication backend """
AUTH_LDAP_SERVER_URI = LDAP_SERVER_URI
AUTH_LDAP_BIND_DN = LDAP_AUTHENTICATION_DN
AUTH_LDAP_BIND_PASSWORD = LDAP_AUTHENTICATION_PASSWORD

AUTH_LDAP_USER_SEARCH = LDAPSearch("ou=users,dc=atilla,dc=org",
                                   ldap.SCOPE_SUBTREE, "(uid=%(user)s)")

AUTH_LDAP_USER_ATTR_MAP = {"first_name": "givenName",
                           "last_name": "sn",
                           "email": "mail"}

AUTH_LDAP_GROUP_SEARCH = LDAPSearch("ou=groups,dc=atilla,dc=org",
                                    ldap.SCOPE_SUBTREE,
                                    "(objectClass=posixGroup)")

AUTH_LDAP_GROUP_TYPE = PosixGroupType()

""" Settings for the accounts app """
MAIL_SENDER = "noreply@members.atilla.org"

LDAP_USERS_BASE_DN = "ou=users,dc=atilla,dc=org"
LDAP_DEFAULT_USER_OU = "users"
LDAP_DEFAULT_GID = 500
LDAP_DEFAULT_HOME_PATH = "/home/users/"
