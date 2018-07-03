# awl.managment.commands.run_script.py
#
# runs the python script given on the command line within the django env

import imp
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """Loads and runs the named python script parameter in this django 
    environment."""

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.help = self.__doc__

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs='+', type=str, 
            help='filename of the python script to run')

    def handle(self, *args, **options):
        imp.load_source('config', options['filename'][0])
