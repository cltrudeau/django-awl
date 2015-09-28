import os, tempfile, shutil
from django.test import TestCase, override_settings

from awl.waelsteng import AdminToolsMixin

from awl.tests.admin import LinkAdmin
from awl.tests.models import Link
from awl.waelsteng import WRunner

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

class GotHere(Exception):
    pass


def fake_loader():
    raise GotHere()


wrunner_settings = {
    'MEDIA_ROOT':'',
    'TEST_DATA':'awl.tests.test_waelsteng.fake_loader',
}


class WRunnerTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tempdir = tempfile.mkdtemp()
        cls.media_dir = os.path.abspath(os.path.join(cls.tempdir, 'media'))
        global wrunner_settings
        wrunner_settings['MEDIA_ROOT'] = cls.media_dir

    def assert_test_strings(self, expected, tests):
        names = [str(test) for test in tests]
        self.assertEqual(set(expected), set(names))

    @override_settings(WRUNNER=wrunner_settings)
    def test_runner(self):
        # hopefully the universe won't implode as we're using our runner to
        # test our runner
        runner = WRunner()

        # check media root handling
        runner.setup_test_environment()
        self.assertTrue(os.path.isdir(self.media_dir))

        # do it again to make sure directory already existing doesn't blow
        # anything up
        runner.setup_test_environment()

        # check test loader
        with self.assertRaises(GotHere):
            runner.setup_databases()

        # -- test various labels work
        expected = [
            'test_same_order (awl.tests.test_ranked.GroupedTests)',
            'test_same_order (awl.tests.test_ranked.AloneTests)',
            'test_too_large (awl.tests.test_ranked.GroupedTests)',
        ]
        suite = runner.build_suite([
            'awl.tests.test_ranked.GroupedTests.test_too_large',
            '=_same_order'])
        self.assert_test_strings(expected, suite)

        # shortcuts only
        expected = [
            'test_same_order (awl.tests.test_ranked.GroupedTests)',
            'test_same_order (awl.tests.test_ranked.AloneTests)',
        ]
        suite = runner.build_suite(['=_same_order'])
        self.assert_test_strings(expected, suite)

        # test no labels at all
        suite = runner.build_suite([])
        self.assertTrue(list(suite))

        # -- check media root cleanup
        runner.teardown_databases(old_config=([], []))
        self.assertFalse(os.path.exists(self.media_dir))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tempdir)
