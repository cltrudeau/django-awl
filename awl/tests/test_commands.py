# awl.tests.test_commands.py
import os, mock

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase

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
