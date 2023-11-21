# awl.utils.py

import django
from django.shortcuts import render
from django.template.loader import render_to_string

# =============================================================================
# Template Methods
# =============================================================================

def render_page(request, page_name, data={}):
    """
    .. deprecated:: 0.12
        Use ``django.shortcuts.render`` instead
    
    This function was a wrapper for ``render_to_response`` that handled
    request context.  The ``django.shortcuts.render`` method does the same
    thing, so this just wraps that now. 
    """
    return render(request, page_name, data)


def render_page_to_string(request, page_name, data={}):
    """A shortcut for using ``render_to_string`` with a
    :class:`RequestContext` automatically.
    """
    return render_to_string(page_name, data, request=request)

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


def get_field_names(obj, ignore_auto=True, ignore_relations=True, 
        exclude=[]):
    """Returns the field names of a Django model object.

    :param obj: the Django model class or object instance to get the fields
        from
    :param ignore_auto: ignore any fields of type AutoField. Defaults to True
    :param ignore_relations: ignore any fields that involve relations such as
        the ForeignKey or ManyToManyField
    :param exclude: exclude anything in this list from the results

    :returns: generator of found field names
    """

    from django.db.models import (AutoField, ForeignKey, ManyToManyField, 
        ManyToOneRel, OneToOneField, OneToOneRel)

    for field in obj._meta.get_fields():
        if ignore_auto and isinstance(field, AutoField):
            continue

        if ignore_relations and (isinstance(field, ForeignKey) or
                isinstance(field, ManyToManyField) or
                isinstance(field, ManyToOneRel) or
                isinstance(field, OneToOneRel) or
                isinstance(field, OneToOneField)):
            # optimization is killing coverage measure, have to put no-op that
            # does something
            a = 1; a
            continue

        if field.name in exclude:
            continue

        yield field.name


def get_obj_attr(obj, attr):
    """Works like getattr() but supports django's double underscore object
    dereference notation.

    Example usage:

    .. code-block:: python

        >>> get_obj_attr(book, 'writer__age')
        42
        >>> get_obj_attr(book, 'publisher__address')
        <Address object at 105a79ac8>

    :param obj: 
        Object to start the derference from

    :param attr:
        String name of attribute to return

    :returns:
        Derferenced object 

    :raises:
        AttributeError in the attribute in question does not exist
    """
    # handle '__' referencing like in QuerySets
    fields = attr.split('__')
    field_obj = getattr(obj, fields[0])

    for field in fields[1:]:
        # keep going down the reference tree
        field_obj = getattr(field_obj, field)

    return field_obj

# ============================================================================
# Misc
# ============================================================================

class URLTree(object):
    """A tree representation of the django url paths.  Each path is stored in
    a dictionary with its regex pattern, full path, name (if available) and
    children.  Root items in the tree can be accessed through the ``children``
    list attribute.
    """
    def __init__(self):
        self.children = []

        # parse the url pattern tree 
        from django.conf import settings
        urlconf = __import__(settings.ROOT_URLCONF, {}, {}, [''])
        self._parse_node(urlconf.urlpatterns, '', self.children)

    def _parse_node(self, parent, parent_path, children):
        for entry in parent:
            # django 1.11 and 2.0 have different URLResolver objects
            if django.VERSION[0] >= 2:
                pattern = entry.pattern.regex.pattern
            else:  # pragma: no cover
                pattern = entry.regex.pattern

            path = parent_path + pattern
            d = {
                'pattern':pattern,
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
