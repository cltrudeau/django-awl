# awl.tests.test_commands.py
import os, mock

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase, override_settings

from waelstow import capture_stdout

# ============================================================================

class CommandTests(TestCase):
    def test_create_admin(self):
        call_command('create_test_admin')

        # verify user created by script exists
        User.objects.get(username='admin')

    def test_run_script(self):
        filename = os.path.abspath(os.path.join(
            os.path.dirname(__file__), 'data/runme.py'))

        call_command('run_script', filename)

        # verify user created by script exists
        User.objects.get(username='fakeuser')

    @mock.patch('os.remove')
    def test_wipe_migrations(self, mocked_remove):
        call_command('wipe_migrations')

        self.assertTrue(mocked_remove.called)

    def test_print_setting(self):
        with override_settings(FOO='thingy'):
            with capture_stdout() as capture:
                call_command('print_setting', 'FOO')

            self.assertEqual(capture.getvalue(), 'thingy\n')

        with override_settings(BAR=['one', 'two']):
            with capture_stdout() as capture:
                call_command('print_setting', 'BAR')

            self.assertEqual(capture.getvalue(), 'one two\n')

        with override_settings(BAZ=('three', 'four')):
            with capture_stdout() as capture:
                call_command('print_setting', 'BAZ')

            self.assertEqual(capture.getvalue(), 'three four\n')
