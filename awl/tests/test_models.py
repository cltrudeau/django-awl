# awl.tests.test_models.py
from django.test import TestCase

from awl.models import Counter, Lock
from awl.utils import refetch
from awl.tests.models import Validator

# ============================================================================

class ModelsTest(TestCase):
    def test_validating_mixin(self):
        # Validator overrides full_clean() to increment its counter,
        # full_clean() is called on every save, so after creation and save the
        # value should be 2
        v = Validator.objects.create()
        v.save()
        v = refetch(v)
        self.assertEqual(2, v.counter)

    def test_counter(self):
        count = Counter.objects.create(name='foo')
        Counter.increment('foo')
        count = refetch(count)
        self.assertEqual(1, count.value)

    def test_lock(self):
        # not much to test here except that it doesn't blow up
        Lock.objects.create(name='foo')
        Lock.lock_until_commit('foo')
