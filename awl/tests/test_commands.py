# awl.tests.test_commands.py
import os
from unittest import mock

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import call_command, CommandError
from django.test import TestCase, override_settings

from context_temp import temp_directory
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

    def test_create_cmd(self):
        with temp_directory(path=settings.BASE_DIR) as td:
            app_name = os.path.basename(td)
            mgm_dir = os.path.join(td, 'management')
            mgm_init = os.path.join(mgm_dir, '__init__.py')
            cmd_dir = os.path.join(mgm_dir, 'commands')
            cmd_init = os.path.join(cmd_dir, '__init__.py')
            cmd_file = os.path.join(cmd_dir, 'cmd.py')
            named_file = os.path.join(cmd_dir, 'named.py')

            # test from scratch
            call_command('create_cmd', app_name)
            self.assertTrue(os.path.isdir(mgm_dir))
            self.assertTrue(os.path.isfile(mgm_init))
            self.assertTrue(os.path.isdir(cmd_dir))
            self.assertTrue(os.path.isfile(cmd_init))
            self.assertTrue(os.path.isfile(cmd_file))

            # test with named file on existing structure
            call_command('create_cmd', app_name, 'named')
            self.assertTrue(os.path.isfile(named_file))

            # test bad app name
            with self.assertRaises(CommandError) as cm:
                call_command('create_cmd', 'foo')

            self.assertIn('No such app', cm.exception.args[0])

            # test no file over-write
            with self.assertRaises(CommandError) as cm:
                call_command('create_cmd', app_name)

            self.assertIn('already existed', cm.exception.args[0])
