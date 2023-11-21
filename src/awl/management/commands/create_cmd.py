# awl.managment.commands.create_cmd.py
#
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

# ===========================================================================

def _create_module(path):
    """Creates module directory if it doesn't exist and its containing
    __init__.py file."""
    if not os.path.isdir(path):
        os.makedirs(path)

    # create __init__.py
    i_file = os.path.join(path, '__init__.py')
    if not os.path.isfile(i_file):
        with open(i_file, 'w'):
            # write and empty file
            pass

# ---------------------------------------------------------------------------

contents = """
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    \"\"\"Command help information goes here

    \"\"\" 

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.help = self.__doc__

    def add_arguments(self, parser):
        # Command uses argparse, this method is called to add arguments
        parser.add_argument('first_arg', type=str,
            help='First argument')

    def handle(self, *args, **options):
        base_dir = settings.BASE_DIR

        # code for your command goes here
        first_arg = options['first_arg']

"""

# ---------------------------------------------------------------------------

class Command(BaseCommand):
    """Creates the directory structure and corresponding file for a django
    command within an app.

    If "cmd_name" is not provided, defaults to "cmd.py"
    """ 

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.help = self.__doc__

    def add_arguments(self, parser):
        parser.add_argument('app_name', type=str,
            help='Name of app to create the file within')
        parser.add_argument('cmd_name', nargs='?', default='cmd',
            help='Name of command to create, defaults to "cmd"')

    def handle(self, *args, **options):
        app_dir = os.path.join(settings.BASE_DIR, options['app_name'])
        if not os.path.isdir(app_dir):
            raise CommandError('No such app found: %s' % options['app_name'])

        # create the modules
        target = os.path.join(app_dir, 'management')
        _create_module(target)
        target = os.path.join(target, 'commands')
        _create_module(target)

        # create the command
        cmd_file = os.path.join(target, '%s.py' % options['cmd_name'])
        if os.path.isfile(cmd_file):
            raise CommandError(('A File named "%s.py" already existed, '
                'aborting') % options['cmd_name'])

        with open(cmd_file, 'w') as f:
            f.write(contents)
