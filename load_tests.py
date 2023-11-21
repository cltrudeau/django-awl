#!/usr/bin/env python
#import os, sys
import sys
from unittest import TestSuite

from boot_django import boot_django

# call the django setup routine
boot_django()

#from django.core.management import call_command
#call_command('shell')

default_labels = ['tests', ]

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
