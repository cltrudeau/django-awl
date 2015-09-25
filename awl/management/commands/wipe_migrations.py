# awl.managment.commands.wipe_migrations.py
#
# searches through the INSTALLED_APP listing looking for any apps that are in
# the same base directory structure as the command and removes any migration
# scripts belonging to them
import os

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        project_dir = settings.BASE_DIR
        search_dir = os.path.abspath(os.path.dirname(project_dir))

        for app in apps.get_apps():
            filename = app.__file__
            if filename.startswith(search_dir):
                app_dir = os.path.abspath(os.path.dirname(filename))
                migrations = os.path.join(app_dir, 'migrations')
                if os.path.isdir(migrations):
                    for filename in os.listdir(migrations):
                        if filename.startswith('_'):
                            continue

                        os.remove(os.path.join(migrations, filename))
