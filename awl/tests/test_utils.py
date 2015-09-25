# awl.tests.test_utils.py
import sys
from django.test import TestCase
from django.http import HttpResponse

from six import StringIO

from awl.tests.models import Link
from awl.utils import (URLTree, refetch, refetch_for_update, render_page,
    render_page_to_string)
from awl.waelsteng import FakeRequest

# ============================================================================

class UtilsTest(TestCase):
    def test_url_tree(self):
        # print_tree() exercises everything, so run it and capture stdout
        tree = URLTree()

        saved_stdout = sys.stderr
        try:
            out = StringIO()
            sys.stdout = out
            tree.print_tree()

            # check for some of our rankedmodel items in the output
            output = out.getvalue().split('\n')
            self.assertIn('rankedmodel/', output)
            self.assertIn(('rankedmodel/move/(\d+)/(\d+)/(\d+)/$, ' 
                'name=awl-rankedmodel-move'), output)

        finally:
            sys.stdout = saved_stdout

    def test_refetch(self):
        link = Link.objects.create(url='url', text='text')
        link.text = 'foo'

        link = refetch(link)
        self.assertEqual('url', link.url)
        self.assertEqual('text', link.text)

        link.text = 'foo'
        link = refetch_for_update(link)
        self.assertEqual('url', link.url)
        self.assertEqual('text', link.text)

    def test_renders(self):
        request = FakeRequest()
        expected = 'Hello World\n'

        result = render_page_to_string(request, 'sample.html', {'name':'World'})
        self.assertEqual(expected, result)

        response = render_page(request, 'sample.html', {'name':'World'})
        self.assertEqual(expected, response.content.decode('ascii'))
