# awl.management.commands.wtest.py
#
# Uses the awl.waelsteng.WRunner to locate and run tests
import sys

from django.core.management.base import BaseCommand

from awl.waelsteng import WRunner

class Command(BaseCommand):
    """
    Uses the awl.waelsteng.WRunner to locate and run tests. WRunner supports
    shortcut test label names. For example "=foo" or ":foo" will look for any
    test suites or cases with 'foo' in their name.
    """

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.help = self.__doc__

    def add_arguments(self, parser):
        parser.add_argument('test_labels', type=str, nargs="*", default=[],
            help='One or more test label to run. Supports "=" shortcuts')

    def handle(self, *args, **options):
        runner = WRunner(verbosity=1)
        failures = runner.run_tests(options['test_labels'])
        if failures:
            sys.exit(failures)
