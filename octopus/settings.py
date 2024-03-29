# Django settings for octopus project.
import os

PROJECT_DIR = os.path.dirname(__file__)

TIME_ZONE = 'GB'

# SESSION_EXPIRE_AT_BROWSER_CLOSE = False

SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SESSION_COOKIE_AGE = 1209600

SESSION_COOKIE_DOMAIN = ".baskettt.co"

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('JD', 'jd@baskettt.co'),
    ('Arnaud', 'arnaud@baskettt.co'),
)

MANAGERS = ADMINS
AUTH_USER_MODEL = 'octopus_user.OctopusUser'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'baskettt@baskettt.co'
EMAIL_HOST_PASSWORD = 's@a46FW4Ak9=3Nig8'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

DATABASES = {
    'default': {
        'ENGINE': 'django_hstore.postgresql_psycopg2',  # Add 'postgresql_psycopg2'
        'NAME': 'db1',

        'USER': 'octopus_user',
        'PASSWORD': 'e9IKyjFIRbDgGPumhyvOOKvGWuV8CPp1xkABMS8abV4p9bKUnO5g7WfCkdk4s1l',
        'HOST': '162.13.177.180', # as of writing this was the adress of octopus_postgres_master
        'PORT': '5435',           # Set to empty string for default.
    }
}

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://162.13.177.216:9201/',
        'INDEX_NAME': 'haystack',
        'INCLUDE_SPELLING': True,
        'TIMEOUT': 120,
    },
}

#HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

FIXTURE_DIRS = [
    'fixtures',
]

ROOT_URLCONF='octopus.urls'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = '/webapps/octopus/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR,'../assets/'),
    os.path.join(PROJECT_DIR,'../bower_components/'),

    #os.path.join(PROJECT_DIR,'../bin/'),

)

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = '/webapps/octopus/static/'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = "/static/"

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'z_=7bw_&mdkt5j%t4mhfu7)f1%xh#4i8_576^h22pnwq$s+m-a'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'octopus_middleware.django-crossdomainxhr-middleware.XsSharing',

    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'octopus.wsgi.application'

TEMPLATE_DIRS = (
    "templates"
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.auth',
    'django_verbatim', #Makes django templates work with angularjs
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',

    # Added
    'django_hstore',  # Support for schemaless in postgress
    'gunicorn',
    'tastypie',
    'corsheaders',
    'south', #brings migration to Django to have stable database-independent migration layer
    'registration',
    'haystack',
    'celery',
    'rest_framework',
    # My apps
    'octopus_groceries',
    'octopus_user',
    'octopus_basket',
    'octopus_middleware',
    'octopus_recommendation_engine',
    'octopus_search_engine',
    'octopus_cron_jobs',
    'webScraper',
)


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.request",
    "django.contrib.auth.context_processors.auth",
)

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
)


SITE_ID = 1

TASTYPIE_FULL_DEBUG = False

TASTYPIE_CANNED_ERROR = "Sorry about that, there's a problem on our end!"

MAX_USERNAME_LENGTH = 150

ACCOUNT_ACTIVATION_DAYS = 7

SOUTH_DATABASE_ADAPTERS = {'default': 'south.db.postgresql_psycopg2'}


ALLOWED_HOSTS = [
    '127.0.0.1',  # localhost
    '.baskettt.co',
    '.baskettt.com',
    '.baskettt.co.uk',
    '.baskettt.net',
]

#Celery stuff

from .celery import crontab
CELERY_IMPORTS = ('octopus_cron_jobs.tasks', ) # just add imports here

BROKER_URL = 'amqp://octopus_rabbitmq_user:octopus_rabbitmq_password@octopus-crawler/octopus_rabbitmq_vhost'
#CELERY_RESULT_BACKEND = 'db+postgresql://octopus@octopus-crawler/db1'

CELERYBEAT_SCHEDULE = {
    # Executes every Monday morning at 7:30 A.M
    'create_recommendations_then_send_email': {
        'task': 'octopus_cron_jobs.tasks.create_recommendations_then_send_email',
        'schedule': crontab(minute=0, hour='17'),
    },

    'sanitize_db': {
        'task': 'octopus_cron_jobs.tasks.sanitize_db',
        'schedule': crontab(minute=0, hour='*/3'),
    },
}

CELERY_TIMEZONE = 'Europe/London'
CELERY_ENABLE_UTC = True


try:
    from local_settings import *
except ImportError:
    pass
