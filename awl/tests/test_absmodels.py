# awl.tests.test_models.py
from django.test import TestCase

from awl.utils import refetch
from awl.tests.models import Validator

# ============================================================================

class AbsModelsTest(TestCase):
    def test_validating_mixin(self):
        # Validator overrides full_clean() to increment its counter,
        # full_clean() is called on every save, so after creation and save the
        # value should be 2
        v = Validator.objects.create()
        v.save()
        v = refetch(v)
        self.assertEqual(2, v.counter)
