# awl.managment.commands.create_test_admin.py
#
# Creates an admin user, done here so it can be automated as part of the reset
# script

from django.core.management.base import BaseCommand
from awl.waelsteng import create_admin

class Command(BaseCommand):
    """Creates a test admin user account by calling
    :func:'awl.waelsteng.create_admin'"""

    help = ('Creates a test admin user account by calling '
        'awl.waelsteng.create_admin')

    def handle(self, *args, **options):
        create_admin()
