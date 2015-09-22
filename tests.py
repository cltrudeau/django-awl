#!/usr/bin/env python

import sys
import django

from django.conf import settings
from django.test.runner import DiscoverRunner

settings.configure(DEBUG=True,
    DATABASES={
        'default':{
            'ENGINE':'django.db.backends.sqlite3',
        }
    },
    ROOT_URLCONF='awl.tests.urls',
    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
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
    ),
)

labels = ['awl.tests', 'awl.rankedmodel.tests']
if len(sys.argv[1:]) > 0:
    labels = sys.argv[1:]

django.setup()

#from awl.waelsteng import WRunner
#from wrench.waelstow import list_tests
#runner = WRunner()
#suite = runner.build_suite(labels)
#for t in list_tests(suite):
#    print(t)
#
#quit()

#runner = DiscoverRunner(verbosity=1)

from awl.waelsteng import WRunner
runner = WRunner(verbosity=1)
failures = runner.run_tests(labels)
if failures:
    sys.exit(failures)
