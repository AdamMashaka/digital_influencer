from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-^!x_%)xs1)#tv6p8t)nqy_-zm7q4#(e2algds%&fl2p2_*l4*s'


DEBUG = True
 

ALLOWED_HOSTS = [
    '127.0.0.1', 
    'localhost', 
    '157.173.105.219', 
    'liveodds.kijanicart.com', 
    'liveodds.games', 
    'adamkatani.systems', 
    'd554-41-59-87-86.ngrok-free.app',   
    'ticevents.onrender.com',
]


CSRF_TRUSTED_ORIGINS =[
    'https://127.0.0.1',
    'https://localhost',
    'https://157.173.105.219',
    'https://liveodds.kijanicart.com', 
    'https://liveodds.games',
    'https://adamkatani.systems',
    'https://d554-41-59-87-86.ngrok-free.app',  
    'https://ticevents.onrender.com',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'influencers',
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

ROOT_URLCONF = 'digital.urls'

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

WSGI_APPLICATION = 'digital.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True



BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587 
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'mashakaadam123@gmail.com'
EMAIL_HOST_PASSWORD = 'ewztowqevbbmipzc' 
DEFAULT_FROM_EMAIL = 'mashakaadam123@gmail.com' 
#ewztowqevbbmipzc
        
        
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGOUT_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL = '/'

APPEND_SLASH = True  


#LOGGING = {
  #  'version': 1,
  #  'disable_existing_loggers': False,
   # 'handlers': {
    #    'console': {
     #       'class': 'logging.StreamHandler',
      #  },
    #},
   # 'loggers': {
    #    'django': {
     #       'handlers': ['console'],
      #      'level': 'DEBUG',
       # },
    #},
#}

