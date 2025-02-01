# tests.test_tags.py

from django.template import Context, Template, TemplateSyntaxError
from django.test import TestCase

from waelstow import noted_raise

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

        # -- test bad key
        data['key'] = 'missing'
        context = Context(data)
        result = template.render(context)
        self.assertEqual('', result.strip())

    def test_accessor(self):
        class Dummy(object):
            pass

        d = Dummy()
        d.one = Dummy()
        d.one.two = {
            'three': {
                'four': 'five',
            }
        }

        context_data = {
            'myobj':d,
            'attr1':'one',
            'key1':'three',
        }

        t = """
        {% load awltags %}
        
        {% accessor myobj attr1 'two' [key1] ['four'] %}
        """

        template = Template(t)
        context = Context(context_data)
        result = template.render(context)
        self.assertEqual('five', result.strip())

        # -- test "as" functionality
        t = """
        {% load awltags %}
        
        {% accessor myobj attr1 'two' [key1] ['four'] as thing %}
        """
        template = Template(t)
        context = Context(context_data)
        result = template.render(context)
        self.assertEqual('', result.strip())
        self.assertEqual('five', context['thing'])

        # -- test failure modes

        # test no attributes
        with self.assertRaises(TemplateSyntaxError):
            t = """
            {% load awltags %}
            
            {% accessor %}
            """

            template = Template(t)

        # test 1 attribute
        with self.assertRaises(TemplateSyntaxError):
            t = """
            {% load awltags %}
            
            {% accessor myobj %}
            """
            template = Template(t)

        # test KeyError results in blank 
        t = """
        {% load awltags %}
        
        {% accessor myobj attr1 'foo' [key1] ['four'] %}
        """
        template = Template(t)
        context = Context(context_data)
        result = template.render(context)
        self.assertEqual('', result.strip())

        # test KeyError results blank context variable
        t = """
        {% load awltags %}
        
        {% accessor myobj attr1 'foo' [key1] ['four'] as thing %}
        """
        template = Template(t)
        context = Context(context_data)
        result = template.render(context)
        self.assertEqual('', result.strip())
        self.assertEqual('', context['thing'])

    def test_nop(self):
        t = "{% load awltags %}{% nop 'thing and stuff' %}"
        
        template = Template(t)
        context = Context({})
        result = template.render(context)
        self.assertEqual('', result)

    def test_jsonify(self):
        t = "{% load awltags %}let actors = {% jsonify actors %};"

        actors = {
            'Pitt':'Brad',
        }
        
        template = Template(t)
        context = Context({'actors':actors})
        result = template.render(context)

        expected = """let actors = {"Pitt": "Brad"};"""
        self.assertEqual(expected, result)

    def test_qif(self):
        data = {
            "good":True,
            "bad":False,
            "car":"Honda",
            "nothing":[],
            "value":3,
            "fruit":["apples", "oranges"],
        }

        tests = [
            ("{% load awltags %}{% qif good 'yes' %}", "yes"),
            ("{% load awltags %}{% qif bad 'no' %}", ""),
            ("{% load awltags %}{% qif foo 'no' %}", ""),
            ("{% load awltags %}{% qif good.0 'no' %}", ""),
            ("{% load awltags %}{% qif good car %}", "Honda"),
            ("{% load awltags %}{% qif nothing 'no' %}", ""),
            ("{% load awltags %}{% qif fruit 'yes' %}", "yes"),
            ("{% load awltags %}{% qif value > 2 'yes' %}", "yes"),

            ("{% load awltags %}{% qifelse good 'yes' 'no'%}", "yes"),
            ("{% load awltags %}{% qifelse bad 'yes' 'no'%}", "no"),
            ("{% load awltags %}{% qifelse nothing 'yes' 'no'%}", "no"),
            ("{% load awltags %}{% qifelse fruit 'yes' 'no'%}", "yes"),
            ("{% load awltags %}{% qifelse value > 2 'yes' 'no'%}", "yes"),
            ("{% load awltags %}{% qifelse value > 4 'yes' 'no'%}", "no"),
        ]

        c = Context(data)
        with noted_raise("Test tag:{tag}"):
            for tag, expected in tests:
                t = Template(tag)
                result = t.render(c)

                self.assertEqual(expected, result)
