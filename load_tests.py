#!/usr/bin/env python
#import os, sys
import sys
from unittest import TestSuite

from boot_django import boot_django

#import django
#from django.conf import settings
#from django.test import SimpleTestCase
#from django.test.runner import DiscoverRunner

# call the django setup routine
boot_django()

#AWL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'awl'))
#
#settings.configure(
#    BASE_DIR=AWL_DIR,
#    DEBUG=True,
#    DATABASES={
#        'default':{
#            'ENGINE':'django.db.backends.sqlite3',
#        }
#    },
#    ROOT_URLCONF='awl.tests.urls',
#    MIDDLEWARE = (
#        'django.middleware.security.SecurityMiddleware',
#        'django.contrib.sessions.middleware.SessionMiddleware',
#        'django.middleware.common.CommonMiddleware',
#        'django.middleware.csrf.CsrfViewMiddleware',
#        'django.contrib.auth.middleware.AuthenticationMiddleware',
#        'django.contrib.messages.middleware.MessageMiddleware',
#        'django.middleware.clickjacking.XFrameOptionsMiddleware',
#    ),
#    INSTALLED_APPS=(
#        'django.contrib.auth',
#        'django.contrib.contenttypes',
#        'django.contrib.sessions',
#        'django.contrib.admin',
#        'awl',
#        'awl.tests',
#    ),
#    TEMPLATES = [{
#        'BACKEND':'django.template.backends.django.DjangoTemplates',
#        'DIRS':[
#            os.path.abspath(os.path.join(AWL_DIR, 'tests/data/templates')),
#        ],
#        'APP_DIRS':True,
#        'OPTIONS': {
#            'context_processors':[
#                'django.template.context_processors.debug',
#                'django.template.context_processors.request',
#                'django.contrib.auth.context_processors.auth',
#                'django.contrib.messages.context_processors.messages',
#            ]
#        }
#    }],
#    WRUNNER = {
#        'CREATE_TEMP_MEDIA_ROOT':True,
#    },
#)
#django.setup()

#from django.core.management import call_command
#call_command('shell')

default_labels = ['awl.tests', ]

def get_suite(labels=default_labels):
    from awl.waelsteng import WRunner
    runner = WRunner(verbosity=1)
    failures = runner.run_tests(labels)
    if failures:
        sys.exit(failures)

    # in case this is called from setup tools, return a test suite
    return TestSuite()


if __name__ == '__main__':
    labels = default_labels
    if len(sys.argv[1:]) > 0:
        labels = sys.argv[1:]

    get_suite(labels)
