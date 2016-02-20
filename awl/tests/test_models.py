# awl.tests.test_models.py
from django.test import TestCase

from awl.models import Counter, Lock
from awl.utils import refetch

# ============================================================================

class ModelsTest(TestCase):
    def test_counter(self):
        count = Counter.objects.create(name='foo')
        Counter.increment('foo')
        count = refetch(count)
        self.assertEqual(1, count.value)

    def test_lock(self):
        # not much to test here except that it doesn't blow up
        Lock.objects.create(name='foo')
        Lock.lock_until_commit('foo')
