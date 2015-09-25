# awl.utils.py

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string

# =============================================================================
# Template Methods
# =============================================================================

def render_page(request, page_name, data={}):
    """A shortcut for using ``render_to_response`` with a
    :class:`RequestContext` automatically.
    """
    return render_to_response(page_name, data,
        context_instance=RequestContext(request))


def render_page_to_string(request, page_name, data={}):
    """A shortcut for using ``render_to_string`` with a
    :class:`RequestContext` automatically.
    """
    return render_to_string(page_name, data,
        context_instance=RequestContext(request))

# ============================================================================
# Object Model Tools
# ============================================================================

def refetch(obj):
    """Queries the database for the same object that is passed in, refetching
    its contents in case they are stale.

    :param obj:
        Object to refetch

    :returns:
        Refreshed version of the object
    """
    return obj.__class__.objects.get(id=obj.id)


def refetch_for_update(obj):
    """Queries the database for the same object that is passed in, refetching
    its contents and runs ``select_for_update()`` to lock the corresponding
    row until the next commit.

    :param obj:
        Object to refetch
    :returns:
        Refreshed version of the object
    """
    return obj.__class__.objects.select_for_update().get(id=obj.id)

# ============================================================================
# Misc
# ============================================================================

class URLTree(object):
    """A tree representation of the django url regexes.  Each pattern is
    stored in a dictionary with its pattern, full path, name (if available)
    and children.  Root items in the tree can be accessed through the
    ``children`` list attribute.
    """
    def __init__(self):
        self.children = []

        # parse the url pattern tree 
        from django.conf import settings
        urlconf = __import__(settings.ROOT_URLCONF, {}, {}, [''])
        self._parse_node(urlconf.urlpatterns, '', self.children)

    def _parse_node(self, parent, parent_path, children):
        for entry in parent:
            path = parent_path + entry.regex.pattern
            d = {
                'pattern':entry.regex.pattern,
                'path':path,
                'name':entry.name if hasattr(entry, 'name') else '',
                'children':[],
            }
            children.append(d)

            if hasattr(entry, 'url_patterns'):
                self._parse_node(entry.url_patterns, path, d['children'])

    def _depth_traversal(self, node, result):
        text = node['path']
        if node['name']:
            text += ', name=%s' % node['name']

        result.append(text)
        for child in node['children']:
            self._depth_traversal(child, result)

    def as_list(self):
        """Returns a list of strings describing the full paths and patterns
        along with the name of the urls.  Example:

        .. code-block::python
            >>> u = URLTree()
            >>> u.as_list()
            [
                'admin/',
                'admin/$, name=index',
                'admin/login/$, name=login',
            ]
        """
        result = []
        for child in self.children:
            self._depth_traversal(child, result)

        return result

    def print_tree(self):
        """Convenience method for printing the results of
        :class:`URLTree.as_list` to STDOUT
        """
        for line in self.as_list():
            print(line)
