# awl.managment.commands.run_script.py
#
# runs the python script given on the command line within the django env

import imp
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Loads (runs) the given python script in the django space'

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs='+', type=str)

    def handle(self, *args, **options):
        imp.load_source('config', options['filename'][0])
