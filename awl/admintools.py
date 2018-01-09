# awl.admintools.py
from django.template import Context, Template
from django.urls import reverse
from django.utils.html import format_html

from awl.utils import get_obj_attr

# ============================================================================

def admin_obj_link(obj, display=''):
    """Returns a link to the django admin change list with a filter set to
    only the object given.

    :param obj:
        Object to create the admin change list display link for
    :param display:
        Text to display in the link.  Defaults to string call of the object
    :returns:
        Text containing HTML for a link
    """
    # get the url for the change list for this object
    url = reverse('admin:%s_%s_changelist' % (obj._meta.app_label,
        obj._meta.model_name))
    url += '?id__exact=%s' % obj.id

    text = str(obj)
    if display:
        text = display

    return format_html('<a href="{}">{}</a>', url, text)


def admin_obj_attr(obj, attr):
    """A safe version of :func:``utils.get_obj_attr`` that returns and empty
    string in the case of an exception or an empty object
    """
    try:
        field_obj = get_obj_attr(obj, attr)
        if not field_obj:
            return ''
    except AttributeError:
        return ''

    return field_obj


def _obj_display(obj, display=''):
    """Returns string representation of an object, either the default or based
    on the display template passed in.
    """
    result = ''
    if not display:
        result = str(obj)
    else:
        template = Template(display)
        context = Context({'obj':obj})
        result = template.render(context)

    return result


def make_admin_obj_mixin(name):
    """This method dynamically creates a mixin to be used with your 
    :class:`ModelAdmin` classes.  The mixin provides utility methods that can
    be referenced in side of the admin object's ``list_display`` and other
    similar attributes.
    
    :param name:
        Each usage of the mixin must be given a unique name for the mixin class
        being created
    :returns:
        Dynamically created mixin class

    The created class supports the following methods:

    .. code-block:: python

        add_obj_ref(funcname, attr, [title, display])


    Django admin ``list_display`` does not support the double underscore
    semantics of object references.  This method adds a function to the mixin
    that returns the ``str(obj)`` value from object relations.

    :param funcname:
        Name of the function to be added to the mixin.  In the admin class
        object that includes the mixin, this name is used in the
        ``list_display`` tuple.
    :param attr:
        Name of the attribute to dereference from the corresponding object,
        i.e. what will be dereferenced.  This name supports double underscore
        object link referencing for ``models.ForeignKey`` members.
    :param title:
        Title for the column of the django admin table.  If not given it
        defaults to a capitalized version of ``attr``
    :param display:
        What to display as the text in the column.  If not given it defaults
        to the string representation of the object for the row: ``str(obj)`` .
        This parameter supports django templating, the context for which
        contains a dictionary key named "obj" with the value being the object
        for the row.

    .. code-block:: python

        add_obj_link(funcname, attr, [title, display])


    This method adds a function to the mixin that returns a link to a django
    admin change list page for the member attribute of the object being
    displayed.

    :param funcname:
        Name of the function to be added to the mixin.  In the admin class
        object that includes the mixin, this name is used in the
        ``list_display`` tuple.
    :param attr:
        Name of the attribute to dereference from the corresponding object,
        i.e. what will be lined to.  This name supports double underscore
        object link referencing for ``models.ForeignKey`` members.
    :param title:
        Title for the column of the django admin table.  If not given it
        defaults to a capitalized version of ``attr``
    :param display:
        What to display as the text for the link being shown.  If not given it
        defaults to the string representation of the object for the row: 
        ``str(obj)`` .  This parameter supports django templating, the context
        for which contains a dictionary key named "obj" with the value being
        the object for the row.

    Example usage:

    .. code-block:: python

        # ---- models.py file ----
        class Author(models.Model):
            name = models.CharField(max_length=100)


        class Book(models.Model):
            title = models.CharField(max_length=100)
            author = models.ForeignKey(Author, on_delete=models.CASCADE)


    .. code-block:: python

        # ---- admin.py file ----
        @admin.register(Author)
        class Author(admin.ModelAdmin):
            list_display = ('name', )


        mixin = make_admin_obj_mixin('BookMixin')
        mixin.add_obj_link('show_author', 'Author', 'Our Authors',
            '{{obj.name}} (id={{obj.id}})')

        @admin.register(Book)
        class BookAdmin(admin.ModelAdmin, mixin):
            list_display = ('name', 'show_author')


    A sample django admin page for "Book" would have the table:

    +---------------------------------+------------------------+
    | Name                            | Our Authors            |
    +=================================+========================+
    | Hitchhikers Guide To The Galaxy | *Douglas Adams (id=1)* |
    +---------------------------------+------------------------+
    | War and Peace                   | *Tolstoy (id=2)*       |
    +---------------------------------+------------------------+
    | Dirk Gently                     | *Douglas Adams (id=1)* |
    +---------------------------------+------------------------+


    Each of the *items* in the "Our Authors" column would be a link to the
    django admin change list for the "Author" object with a filter set to show
    just the object that was clicked.  For example, if you clicked "Douglas
    Adams (id=1)" you would be taken to the Author change list page filtered
    just for Douglas Adams books.

    The ``add_obj_ref`` method is similar to the above, but instead of showing
    links, it just shows text and so can be used for view-only attributes of
    dereferenced objects.
    """
    @classmethod
    def add_obj_link(cls, funcname, attr, title='', display=''):
        if not title:
            title = attr.capitalize()

        # python scoping is a bit weird with default values, if it isn't
        # referenced the inner function won't see it, so assign it for use
        _display = display

        def _link(self, obj):
            field_obj = admin_obj_attr(obj, attr)
            if not field_obj:
                return ''

            text = _obj_display(field_obj, _display)
            return admin_obj_link(field_obj, text)
        _link.short_description = title
        _link.allow_tags = True
        _link.admin_order_field = attr

        setattr(cls, funcname, _link)

    @classmethod
    def add_obj_ref(cls, funcname, attr, title='', display=''):
        if not title:
            title = attr.capitalize()

        # python scoping is a bit weird with default values, if it isn't
        # referenced the inner function won't see it, so assign it for use
        _display = display

        def _ref(self, obj):
            field_obj = admin_obj_attr(obj, attr)
            if not field_obj:
                return ''

            return _obj_display(field_obj, _display)
        _ref.short_description = title
        _ref.allow_tags = True
        _ref.admin_order_field = attr

        setattr(cls, funcname, _ref)

    klass = type(name, (), {})
    klass.add_obj_link = add_obj_link
    klass.add_obj_ref = add_obj_ref
    return klass
