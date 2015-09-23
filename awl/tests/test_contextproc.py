# awl.tests.test_contextproc.py

from django.test import TestCase

from awl.context_processors import extra_context
from awl.waelsteng import FakeRequest

# ============================================================================

class ContextProcessorTest(TestCase):
    def test_extra_context(self):
        request = FakeRequest()
        context = extra_context(request)

        self.assertEqual(request, context['request'])
        self.assertEqual('test_host', context['HOST'])
        self.assertFalse(context['IN_ADMIN'])
