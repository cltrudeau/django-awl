# awl.management.commands.run_script.py
#
# runs the python script given on the command line within the Django env

import importlib
import sys
from pathlib import Path

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """Loads and runs the named python script parameter in this Django
    environment."""

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.help = self.__doc__

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str,
            help='filename of the python script to run')

    def handle(self, *args, **options):
        path = Path(options['filename']).resolve()
        sys.path.insert(0, str(path.parent))
        importlib.import_module(path.stem)
