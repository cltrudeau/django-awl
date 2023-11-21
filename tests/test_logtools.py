from django.test import TestCase

from awl.logtools import django_logging_dict

# ============================================================================

class LogToolsTests(TestCase):
    def test_django_logging_dict(self):
        # not much to test here besides that it doesn't blow up
        django_logging_dict('foo')
