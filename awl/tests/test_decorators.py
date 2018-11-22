# awl.tests.test_decorators.py
import json

from django.test import TestCase
from django.http import Http404

from awl.decorators import post_required, json_post_required
from awl.waelsteng import FakeRequest
from logthing.utils import silence_logging

# ============================================================================

class Worked(Exception):
    pass


@post_required
def post_view1(request):
    raise Worked()


@post_required(['foo'])
def post_view2(request):
    raise Worked()


@json_post_required('json_data', 'deserialized')
def json_post_view(request):
    return request.deserialized


@json_post_required('json_data')
def json_post_view2(request):
    return request.json_data

# ============================================================================

class DecoratorTest(TestCase):
    @silence_logging
    def test_post_required(self):
        request = FakeRequest()
        with self.assertRaises(Http404):
            post_view1(request)

        request = FakeRequest(method='POST')
        with self.assertRaises(Worked):
            post_view1(request)

        request = FakeRequest(method='POST', data={ 'foo':'bar', })
        with self.assertRaises(Worked):
            post_view2(request)

        request.POST = {
            'bar':'bar',
        }
        with self.assertRaises(Http404):
            post_view2(request)

    @silence_logging
    def test_json_post_required(self):
        # check that it ensures POST
        request = FakeRequest()
        with self.assertRaises(Http404):
            json_post_view(request)

        # check that it ensures post data
        request = FakeRequest(method='POST')
        with self.assertRaises(Http404):
            json_post_view(request)

        # good case
        content = { 'foo':'bar', }
        data = {
            'json_data':json.dumps(content),
        }
        request = FakeRequest(method='POST', data=data)
        result = json_post_view(request)
        self.assertEqual(content, result)

        # good case with optional request_name
        result = json_post_view2(request)
        self.assertEqual(content, result)
