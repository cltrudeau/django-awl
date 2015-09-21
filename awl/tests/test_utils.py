# awl.tests.test_utils.py
import sys
from django.test import TestCase

from six import StringIO

from awl.utils import URLTree

# ============================================================================

class UtilsTest(TestCase):
    def test_url_tree(self):
        # print_tree() exercises everything, so run it and capture stdout
        tree = URLTree()

        saved_stdout = sys.stderr
        try:
            out = StringIO()
            sys.stdout = out
            tree.print_tree()

            # check for some of our rankedmodel items in the output
            output = out.getvalue().split('\n')
            self.assertIn('rankedmodel/', output)
            self.assertIn(('rankedmodel/move/(\d+)/(\d+)/(\d+)/$, ' 
                'name=awl-rankedmodel-move'), output)

        finally:
            sys.stdout = saved_stdout
