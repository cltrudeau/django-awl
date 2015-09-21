# awl.tests.test_decorators.py

from django.test import TestCase
from django.http import Http404

from awl.decorators import post_required
from awl.waelsteng import FakeRequest
from wrench.logtools.utils import silence_logging

# ============================================================================

class Worked1(Exception):
    pass

class Worked2(Exception):
    pass


@post_required
def view1(request):
    raise Worked1()


@post_required(['foo'])
def view2(request):
    raise Worked2()

# ============================================================================

class DecoratorTest(TestCase):
    @silence_logging
    def test_post_required(self):
        request = FakeRequest()
        with self.assertRaises(Http404):
            view1(request)

        request = FakeRequest(method='POST')
        with self.assertRaises(Worked1):
            view1(request)

        request = FakeRequest(method='POST', data={ 'foo':'bar', })
        with self.assertRaises(Worked2):
            view2(request)

        request.POST = {
            'bar':'bar',
        }
        with self.assertRaises(Http404):
            view2(request)
