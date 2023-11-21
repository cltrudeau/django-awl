# awl.managment.commands.wipe_migrations.py
#
import os

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Searches through the INSTALLED_APP listing looking for any apps that
    are in the same base directory structure as the command and removes any
    migration scripts belonging to them.""" 

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.help = self.__doc__

    def handle(self, *args, **options):
        project_dir = settings.BASE_DIR
        search_dir = os.path.abspath(os.path.dirname(project_dir))

        for app_name in settings.INSTALLED_APPS:
            module = __import__(app_name)
            filename = module.__file__

            if filename.startswith(search_dir):
                app_dir = os.path.abspath(os.path.dirname(filename))
                migrations = os.path.join(app_dir, 'migrations')
                if os.path.isdir(migrations):
                    for filename in os.listdir(migrations):
                        if filename.startswith('_'):
                            continue

                        os.remove(os.path.join(migrations, filename))
