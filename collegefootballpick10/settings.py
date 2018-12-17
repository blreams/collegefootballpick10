"""
Django settings for collegefootballpick10 project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import sys
import os
import ast
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
STATIC_PATH = os.path.join(BASE_DIR, 'static')
TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = ')qrym+f!gm*^c4fwf#sykrx4n)nhfv1+=@a5v_w4qk*z!fw@f('
SECRET_KEY = os.environ.get('COLLEGEFOOTBALLPICK10_DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = True
DEBUG = ast.literal_eval(os.environ.get('COLLEGEFOOTBALLPICK10_DJANGO_DEBUG', 'True'))

ALLOWED_HOSTS = [
    'collegefootballpick10.pythonanywhere.com',
    'blreams.pythonanywhere.com',
    'localhost',
    'jkt-myth',
    'skx-linux',
]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pick10',
    'registration',
    'dbbackup',
)

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'collegefootballpick10.urls'

WSGI_APPLICATION = 'collegefootballpick10.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
if os.environ.get('COLLEGEFOOTBALLPICK10_DATABASE') == 'mysql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get('COLLEGEFOOTBALLPICK10_DATABASE_NAME'),
            'HOST': os.environ.get('COLLEGEFOOTBALLPICK10_DATABASE_HOST'),
            'PORT': '3306',
            'USER': os.environ.get('COLLEGEFOOTBALLPICK10_DATABASE_USER'),
            'PASSWORD': os.environ.get('COLLEGEFOOTBALLPICK10_DATABASE_PASSWORD'),
            'OPTIONS': {'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",},
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Since default port 8081 is in use on my system, adding this
os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = 'localhost:8881'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
        STATIC_PATH,
        )
STATIC_ROOT = os.path.join(BASE_DIR, '../static')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_PATH],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        }
    },
]

#AUTH_PROFILE_MODULE = 'pick10.UserProfile'
REGISTRATION_OPEN = True             # If True, users can register
ACCOUNT_ACTIVATION_DAYS = 7          # One week activation window
REGISTRATION_AUTO_LOGIN = True       # If True, the user will be automatically logged in
LOGIN_REDIRECT_URL = '/pick10/'      # The page you want users to arrive at upon successful login
LOGIN_URL = '/accounts/login/'       # The page users are directed to if they are not logged in

# The following settins are specific to sending email:
EMAIL_USE_TLS = True
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'collegefootballpick10'
EMAIL_HOST_PASSWORD = os.environ.get('COLLEGEFOOTBALLPICK10_GMAIL_PASSWORD')
DEFAULT_FROM_EMAIL = 'collegefootballpick10@gmail.com'
DEFAULT_TO_EMAIL = 'fluffgazer@hotmail.com'

# The following sets up the memcache to use
DISABLE_MEMCACHE = ast.literal_eval(os.environ.get('COLLEGEFOOTBALLPICK10_DISABLE_MEMCACHE', 'False'))
if not DISABLE_MEMCACHE:
    CACHES = {
        'default': {
             'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
             'LOCATION': 'memcache_table',
             'TIMEOUT':None
        }
    }
else:
    CACHES = {
        'default': {
             'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }

SELENIUM_WEBDRIVER_STRING = 'firefox'
if os.environ.get('COLLEGEFOOTBALLPICK10_SELENIUM_WEBDRIVER'):
    SELENIUM_WEBDRIVER_STRING = os.environ.get('COLLEGEFOOTBALLPICK10_SELENIUM_WEBDRIVER')

DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {
        'location': os.path.join(BASE_DIR, '../dbbackup'),
        }

