# awl.tests.test_admintools.py
from django.test import TestCase
from django.contrib.admin.utils import label_for_field

from wrench.utils import parse_link

from awl.waelsteng import AdminToolsMixin
from awl.tests.models import Nested, Inner, Outer
from awl.tests.admin import InnerAdmin, OuterAdmin

# ============================================================================

class AdminToolsTest(TestCase, AdminToolsMixin):
    def test_admin_obj_mixin(self):
        # setup the admin site and id
        self.initiate()

        inner_admin = InnerAdmin(Inner, self.site)
        outer_admin = OuterAdmin(Outer, self.site)

        n1 = Nested.objects.create(name='n1')
        i1 = Inner.objects.create(name='i1', nested=n1)
        o1 = Outer.objects.create(name='o1', inner=i1)

        # check the basic __str__ named link from Inner to Nested
        html = self.field_value(inner_admin, i1, 'show_nested')
        url, text = parse_link(html)
        self.assertEqual('Nested(id=1 n1)', text)
        self.assertEqual('/admin/tests/nested/?id__exact=1', url)

        # check the template based name link of Inner from Outer
        html = self.field_value(outer_admin, o1, 'show_inner')
        url, text = parse_link(html)
        self.assertEqual('Inner.id=1', text)
        self.assertEqual('/admin/tests/inner/?id__exact=1', url)

        # check the double dereferenced Nested from Outer
        html = self.field_value(outer_admin, o1, 'show_nested')
        url, text = parse_link(html)
        self.assertEqual('Nested(id=1 n1)', text)
        self.assertEqual('/admin/tests/nested/?id__exact=1', url)

        # check the title got set correctly
        label = label_for_field('show_inner', o1, outer_admin)
        self.assertEqual(label, 'My Inner')

        # check that empty values work properly
        o2 = Outer.objects.create(name='o2')
        result = self.field_value(outer_admin, o2, 'show_nested')
        self.assertEqual('', result)

        i2 = Inner.objects.create(name='i2')
        o2.inner = i2
        o2.save()
        result = self.field_value(outer_admin, o2, 'show_nested')
        self.assertEqual('', result)
