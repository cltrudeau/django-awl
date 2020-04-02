# awl.tests.test_utils.py
import sys
from io import StringIO

from django.test import TestCase

from awl.tests.models import Link
from awl.utils import (URLTree, refetch, refetch_for_update, render_page,
    render_page_to_string, get_field_names, get_obj_attr)
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

    def test_get_field_names(self):
        from awl.tests.models import Person

        # test defaults, ignore order
        expected = ['name', 'phone']
        result = get_field_names(Person)
        self.assertEqual(set(result), set(expected))

        # test ignore_auto, ignore_relations and exclude
        expected.extend(['id', 'building', 'address', 'courses', 'best_friend',
            'person'])
        expected.remove('phone')
        result = get_field_names(Person, ignore_auto=False,
            ignore_relations=False, exclude=['phone'])
        self.assertEqual(set(result), set(expected))

    def test_get_obj_attr(self):

        # --- data for testing
        class Character(object):
            pass

        class Cartoon(object):
            pass

        barney = Character()
        barney.name = 'Barney'
        betty = Character()
        betty.name = 'Betty'
        betty.husband = barney
        wilma = Character()
        wilma.name = 'Wilma'
        wilma.friend = betty

        cartoon = Cartoon()
        cartoon.name = 'Flinstones'
        cartoon.character = wilma

        # --- tests
        self.assertEqual('Flinstones', get_obj_attr(cartoon, 'name'))
        self.assertEqual(wilma, get_obj_attr(cartoon, 'character'))
        self.assertEqual(betty, get_obj_attr(cartoon, 'character__friend'))
        self.assertEqual(barney, get_obj_attr(cartoon,
            'character__friend__husband'))

        with self.assertRaises(AttributeError):
            get_obj_attr(cartoon, 'foo')

        with self.assertRaises(AttributeError):
            get_obj_attr(cartoon, 'character__foo')
