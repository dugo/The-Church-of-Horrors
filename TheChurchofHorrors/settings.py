# coding=utf-8
# Django settings for TheChurchofHorrors project.

import os.path,site,sys
from distutils.sysconfig import get_python_lib

DEBUG = True
TEMPLATE_DEBUG = DEBUG

PROJECT_ROOT        = os.path.dirname(__file__)
VIRTUALENV_ROOT     = os.path.join(PROJECT_ROOT, '..',"thechurch-env")
SITE_ROOT           = os.path.join(PROJECT_ROOT, 'site')
MODULES_ROOT        = os.path.join(PROJECT_ROOT, 'modules')
APPS_ROOT        = os.path.join(PROJECT_ROOT, 'apps')
SITEPACKAGES_ROOT   = get_python_lib()

sys.path.insert(0, APPS_ROOT)
sys.path.insert(0, MODULES_ROOT)

ADMINS = (
    (u'Rubén Dugo', 'rdugomartin@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'thechurchofhorrors',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': 'root',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Madrid'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es-es'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(SITE_ROOT,"media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = 'http://media.thechurchofhorrors.com/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(MEDIA_ROOT,"static")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = 'http://media.thechurchofhorrors.com/static/'

ADMIN_MEDIA_PREFIX = 'http://media.thechurchofhorrors.com/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    ("admin_tools", os.path.join(MODULES_ROOT,"admin_tools","media","admin_tools")),
    ("tiny_mce", os.path.join(SITEPACKAGES_ROOT,"tinymce","static","tiny_mce")),
    ("filebrowser", os.path.join(MODULES_ROOT,"filebrowser","media","filebrowser")),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '8%y=tan3g33+%($$5wkaf0fa8z7v$n0qo62c0!+y&mj0^c^z1j'

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
    #'TheChurchofHorrors.site.middleware.CommonBlogMiddleware',
    #'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'TheChurchofHorrors.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(SITE_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'filebrowser',
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    
    'blog',
    'userprofile',
    'tinymce',
)

TEMPLATE_CONTEXT_PROCESSORS =(
    "django.contrib.auth.context_processors.auth",
    'django.core.context_processors.request',
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    #"django.contrib.messages.context_processors.messages",
    'django.core.context_processors.request',
    'TheChurchofHorrors.site.context_processors.common',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
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

AUTH_PROFILE_MODULE = 'userprofile.UserProfile'

ADMIN_TOOLS_MENU = 'TheChurchofHorrors.site.menu.CustomMenu'
ADMIN_TOOLS_INDEX_DASHBOARD = 'TheChurchofHorrors.site.dashboard.CustomIndexDashboard'

try:
    from local_settings import *
except ImportError:
    pass


if DEBUG:
    ADMIN_MEDIA_PREFIX  = '/static/admin/'
    STATIC_URL          = '/static/'
    MEDIA_URL           = '/media/'

FILEBROWSER_URL_FILEBROWSER_MEDIA = STATIC_URL+"filebrowser/"
FILEBROWSER_URL_TINYMCE = STATIC_URL+'tiny_mce/'
FILEBROWSER_EXTENSIONS = {
    'Folder': [''],
    'Image': ['.jpg','.jpeg','.gif','.png','.tif','.tiff'],
}

TINYMCE_JS_URL = STATIC_URL+'tiny_mce/tiny_mce_src.js'
TINYMCE_DEFAULT_CONFIG = {
    'plugins': "table,spellchecker,paste,searchreplace",
    'theme': "advanced",
}
TINYMCE_SPELLCHECKER = True
TINYMCE_COMPRESSOR = False

BLOG_MAX_LAST_ENTRIES = 4
