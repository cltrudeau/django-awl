#!/usr/bin/env python

import sys, django

from django.conf import settings
from django.core.management import call_command

settings.configure(
    DEBUG=True,
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'awl',
    ],
)

django.setup()
call_command('makemigrations', 'awl')
