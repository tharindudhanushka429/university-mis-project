import os
from pathlib import Path
import dj_database_url # Database URL සඳහා

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------------------------------------------
# 1. SECRET KEY (වැදගත්!)
# -----------------------------------------------------------------
# පහත පේළිය මකා, ඔබ 36.1 පියවරේදී කොපි කර ගත් 
# ඔබේම SECRET_KEY එක මෙතනට පේස්ට් කරන්න.
SECRET_KEY = 'django-insecure-w$9jefq0g#mu$nf6%!e^-*rbmn1r&f6=m#0texjb+#7dlr__0n'

# -----------------------------------------------------------------
# 2. DEBUG සහ ALLOWED_HOSTS (Production සඳහා)
# -----------------------------------------------------------------
# DEBUG අගය 'False' ලෙස සකසයි, නමුත් පරිසර විචල්‍යයකින් (Env Var) 
# 'True' කළ හැක.
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# Render.com හි ලිපිනය ස්වයංක්‍රීයව එක් කර ගනී
ALLOWED_HOSTS = ['127.0.0.1']

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Render.com වෙතින් POST ඉල්ලීම් විශ්වාස කිරීම
CSRF_TRUSTED_ORIGINS = [f'https://{RENDER_EXTERNAL_HOSTNAME}'] if RENDER_EXTERNAL_HOSTNAME else []


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # WhiteNoise සඳහා
    'whitenoise.runserver_nostatic', 
    'django.contrib.staticfiles',
    'core', # අපේ App එක
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise Middleware (CSS සඳහා)
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'university_mis.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'university_mis.wsgi.application'


# -----------------------------------------------------------------
# 3. DATABASE (Production - PostgreSQL සඳහා)
# -----------------------------------------------------------------
# මෙම කේතය මගින්:
# 1. Render.com හිදී, එය ස්වයංක්‍රීයව 'DATABASE_URL' එක ලබාගෙන 
#    PostgreSQL භාවිතා කරයි.
# 2. ඔබේ පරිගණකයේ (Local), 'DATABASE_URL' එකක් නැති නිසා, 
#    එය නැවත db.sqlite3 ගොනුවක් සාදා ගනී.

DATABASES = {
    'default': dj_database_url.config(
        # db.sqlite3 වෙත නැවත යොමු වීම (fallback)
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600
    )
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# -----------------------------------------------------------------
# 4. STATIC FILES (CSS/JS - WhiteNoise සඳහා)
# -----------------------------------------------------------------
STATIC_URL = '/static/'
# `runserver` භාවිතා නොකරන විට, CSS ගොනු මෙතැනින් පෙන්වයි
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# කාර්යක්ෂමතාව (efficiency) සඳහා WhiteNoise ගබඩාව
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Login URL (වෙනසක් නැත)
LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = 'home'