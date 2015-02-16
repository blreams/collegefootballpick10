"""
Django settings for collegefootballpick10 project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
STATIC_PATH = os.path.join(BASE_DIR, 'static')
TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')qrym+f!gm*^c4fwf#sykrx4n)nhfv1+=@a5v_w4qk*z!fw@f('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_browserid',
    'pick10',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'django_browserid.auth.AutoLoginBackend',
    'django_browserid.auth.BrowserIDBackend',
)

ROOT_URLCONF = 'collegefootballpick10.urls'

WSGI_APPLICATION = 'collegefootballpick10.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

mysqldb_name = 'collegefootballpick10'
local_user = os.environ.get('USER')
if local_user is not None:
    mysqldb_name += '_' + local_user

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        #'ENGINE': 'django.db.backends.mysql',
        #'NAME': mysqldb_name,
        #'HOST': '127.0.0.1',
        #'PORT': '3306',
        #'USER': 'user_django',
        #'PASSWORD': 'pass_django',
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
#STATIC_ROOT = os.path.join(BASE_DIR, '../static')

TEMPLATE_DIRS = [
        # Put strings here, like '/home/html/django_templates'.
        # Always use forward slashes, even for Windows.
        # Don't forget to use absolute paths, not relative paths.
        TEMPLATE_PATH,
        ]

# The following are related to browserid
BROWSERID_AUTOLOGIN_EMAIL = 'aaa@bbb.com'
BROWSERID_AUTOLOGIN_ENABLED = True
LOGIN_REDIRECT_URL = '/'

