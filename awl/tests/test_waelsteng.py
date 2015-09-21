from django.test import TestCase

from awl.waelsteng import AdminToolsMixin

from awl.tests.admin import LinkAdmin
from awl.tests.models import Link

# ============================================================================

class AdminMixinTest(TestCase, AdminToolsMixin):
    def setUp(self):
        self.initiate()

    def test_mixin(self):
        link1 = Link.objects.create(url='/admin/', text='Admin')
        link2 = Link.objects.create(url='', text='Blank')
        link_admin = LinkAdmin(Link, self.site)

        self.authed_get('/admin/')
        self.authed_post('/admin/', {})

        expected = ('url', 'text', 'visit_me')
        self.assertEqual(expected, self.field_names(link_admin))
        self.assertEqual('Admin', self.field_value(link_admin, link1, 'text'))

        self.visit_admin_link(link_admin, link1, 'visit_me')
        with self.assertRaises(AttributeError):
            self.visit_admin_link(link_admin, link2, 'visit_me')


    def test_coverate(self):
        # miscellaneous pieces to get our coverage to 100%

        # test before get, to check that auth call worked
        self.authed_post('/admin/', {})

# ============================================================================


