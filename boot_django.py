# File sets up the django environment, used by other scripts that need to
# execute in django land
import sys
from pathlib import Path
import django
from django.conf import settings

def boot_django():
    AWL_DIR = Path("awl").resolve()
    TEST_DIR = Path("tests").resolve()

    sys.path.insert(0, str(TEST_DIR))

    settings.configure(
        BASE_DIR=AWL_DIR,
        SECRET_KEY = 'django-insecure-$w7!y3g6a5i65_k*+wxhp@)@89!@5)spii+pl=_nbo%rm)%74p',
        DEBUG=True,
        DEFAULT_AUTO_FIELD='django.db.models.AutoField',
        DATABASES={
            'default':{
                'ENGINE':'django.db.backends.sqlite3',
                'NAME': str(AWL_DIR / 'db.sqlite3'),
            }
        },
        ROOT_URLCONF='tests.urls',
        MIDDLEWARE = (
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ),
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.admin',
            'awl',
            'tests',
        ),
        TEMPLATES = [{
            'BACKEND':'django.template.backends.django.DjangoTemplates',
            'DIRS':[
                str(TEST_DIR / 'data/templates'),
            ],
            'APP_DIRS':True,
            'OPTIONS': {
                'context_processors':[
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ]
            }
        }],
        WRUNNER = {
            'CREATE_TEMP_MEDIA_ROOT':True,
        },
    )
    django.setup()
