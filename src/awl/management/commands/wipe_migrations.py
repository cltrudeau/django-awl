# awl.managment.commands.wipe_migrations.py
from pathlib import Path

from django.apps import apps, AppConfig
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
        for config in apps.get_app_configs():
            if not isinstance(config, AppConfig):
                # Ignore other config classes
                continue

            project_dir = str(settings.BASE_DIR)
            if not config.path.startswith(project_dir):
                # Ignore anything that isn't a subfolder of the project
                continue

            # Got here: config is AppConfig and a sub-folder of the project
            dirpath = Path(config.path)
            migrations = dirpath / "migrations"
            if not migrations.exists():
                continue

            for path in migrations.iterdir():
                if not path.is_file():
                    # Ignore anything but files
                    continue

                if path.name.startswith("_"):
                    # Ignore special files
                    continue

                path.unlink()
