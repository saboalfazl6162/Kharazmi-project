from os.path import join as joinpath
from os import getenv
from dotenv import load_dotenv
from pathlib import Path


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = getenv('SECRET_KEY')

DEBUG = getenv("DEBUG", "False").lower() in ("true", "1", "yes")

ALLOWED_HOSTS =  getenv("ALLOWED_HOSTS", "").split(",")

DJANGO_APPS = [
    "admin_interface", 
    "colorfield",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]

THIRD_PARTY_APPS = [
    "django_summernote"
]

LOCAL_APPS = [
    "apps.core",
    "apps.users",
    "apps.news",
    "apps.qa"
]


INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'config.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [joinpath(BASE_DIR,"templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': joinpath(BASE_DIR/"database.db"),
    }
}

# auth settings
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
]
AUTH_USER_MODEL = "users.CustomUser"

LOGOUT_REDIRECT_URL = "home-page"

LOGIN_URL = 'login'

LANGUAGE_CODE = 'fa-IR'
USE_I18N = True  
USE_L10N = True
USE_TZ = True
LANGUAGES = [
    ('en', 'English'),
    ('fa', 'Farsi'),
]
LOCALE_PATHS = [
    joinpath(BASE_DIR, 'locale'),
]

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = False

# static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    joinpath(BASE_DIR,"static"),
]
# media files
MEDIA_URL = '/media/'
MEDIA_ROOT = joinpath(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# django_summernote config
SUMMERNOTE_CONFIG = {
    'iframe': True,
    'summernote': {
        'width': '550px',
        'height': '500px',
        'lang': 'fa-IR',
        'toolbar': [
            ['style', ['style']],
            ['font', ['bold', 'italic', 'underline', 'clear']],
            ['para', ['ul', 'ol', 'paragraph']],
            ['insert', ['link', 'picture', 'video']],
            ['view', ['fullscreen', 'codeview', 'help']],
        ],
    },
}
