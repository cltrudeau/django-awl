# awl.managment.commands.print_setting.py
#
# Takes the name of a django setting and prints the result to the screen. 

from django.conf import settings
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """Prints the named django setting to the screen. If the setting is a list
    or tuple, it prints each item in a single line separated by spaces so that
    it can be used as arguments to a command.  """

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.help = self.__doc__

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, 
            help='name of django setting to print')

    def handle(self, *args, **options):
        value = getattr(settings, options['name'])
        if isinstance(value, list) or isinstance(value, tuple):
            value = ' '.join(value)

        print(value)
