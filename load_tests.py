#!/usr/bin/env python
import os, sys
from unittest import TestSuite

import django
from django.conf import settings
from django.test import SimpleTestCase
from django.test.runner import DiscoverRunner

AWL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'awl'))

settings.configure(
    BASE_DIR=AWL_DIR,
    DEBUG=True,
    DATABASES={
        'default':{
            'ENGINE':'django.db.backends.sqlite3',
        }
    },
    ROOT_URLCONF='awl.tests.urls',
    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    ),
    INSTALLED_APPS=(
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.admin',
        'awl',
        'awl.tests',
    ),
    TEMPLATE_DIRS = (
        os.path.abspath(os.path.join(AWL_DIR, 'tests/data/templates')),
    )
)
django.setup()

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
