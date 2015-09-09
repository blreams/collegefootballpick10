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
#SECRET_KEY = ')qrym+f!gm*^c4fwf#sykrx4n)nhfv1+=@a5v_w4qk*z!fw@f('
SECRET_KEY = os.environ.get('COLLEGEFOOTBALLPICK10_DJANGO_SECRET_KEY')

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
    'pick10',
    'registration',
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
            'NAME': 'collegefootballpick10',
            'HOST': 'localhost',
            'PORT': '3306',
            'USER': os.environ.get('COLLEGEFOOTBALLPICK10_DATABASE_USER'),
            'PASSWORD': os.environ.get('COLLEGEFOOTBALLPICK10_DATABASE_PASSWORD'),
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
CACHES = {
    'default': {
         'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
         'LOCATION': 'memcache_table',
         'TIMEOUT':None
    }
}

REGISTRATION_BACKEND_STRING = 'registration.backends.simple.urls'
if os.environ.get('COLLEGEFOOTBALLPICK10_REGISTRATION_BACKEND') is not None:
    REGISTRATION_BACKEND_STRING.replace('simple', os.environ.get('COLLEGEFOOTBALLPICK10_REGISTRATION_BACKEND'))


SELENIUM_WEBDRIVER_STRING = 'firefox'
if os.environ.get('COLLEGEFOOTBALLPICK10_SELENIUM_WEBDRIVER'):
    SELENIUM_WEBDRIVER_STRING = os.environ.get('COLLEGEFOOTBALLPICK10_SELENIUM_WEBDRIVER')

