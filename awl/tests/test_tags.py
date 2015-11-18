# awl.tests.test_tags.py

from django.template import Context, Template
from django.test import TestCase

# ============================================================================

class TagTests(TestCase):

    def test_getitem(self):
        t = """
        {% load awltags %}
        
        {{d|getitem:key}}"""

        template = Template(t)
        data = {
            'd': {
                'foo':'bar',
            },
            'key':'foo',
        }
        context = Context(data)
        result = template.render(context)
        self.assertEqual('bar', result.strip())
