# awl.admintools.py
from django.contrib.admin import ModelAdmin
from django.contrib.admin.utils import lookup_field
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

# ============================================================================
# Newer Admin Object Mechanism

klass_count = 0

class FancyModelAdmin(ModelAdmin):
    """A replacement for :class:`admin.ModelAdmin` which provides additional
    methods for improving how the ``list_display`` attribute works. 

    This class should not be instantiated directly, instead call 
    :func:`fancy_modeladmin`.
    """
    list_display = []

    @classmethod
    def add_displays(cls, *args):
        """Each arg is added to the ``list_display`` property without any
        extra wrappers, using only the regular django functionality"""
        for arg in args:
            cls.list_display.append(arg)

    @classmethod
    def add_display(cls, attr, title=''):
        """Adds a ``list_display`` property without any extra wrappers,
        similar to :func:`add_displays`, but can also change the title.

        :param attr:
            Name of the attribute to add to the display

        :param title:
            Title for the column of the django admin table.  If not given it
            defaults to a capitalized version of ``attr``
        """
        global klass_count
        klass_count += 1
        fn_name = 'dyn_fn_%d' % klass_count
        cls.list_display.append(fn_name)

        if not title:
            title = attr.capitalize()

        def _ref(self, obj):
            # use the django mechanism for field value lookup
            _, _, value = lookup_field(attr, obj, cls)
            return value
        _ref.short_description = title
        _ref.allow_tags = True
        _ref.admin_order_field = attr

        setattr(cls, fn_name, _ref)

    @classmethod
    def add_link(cls, attr, title='', display=''):
        """Adds a ``list_display`` attribute that appears as a link to the
        django admin change page for the type of object being shown. Supports
        double underscore attribute name dereferencing.

        :param attr:
            Name of the attribute to dereference from the corresponding
            object, i.e. what will be lined to.  This name supports double
            underscore object link referencing for ``models.ForeignKey``
            members.

        :param title:
            Title for the column of the django admin table.  If not given it
            defaults to a capitalized version of ``attr``

        :param display:
            What to display as the text for the link being shown.  If not
            given it defaults to the string representation of the object for
            the row: ``str(obj)`` .  This parameter supports django
            templating, the context for which contains a dictionary key named
            "obj" with the value being the object for the row.

        Example usage:

        .. code-block:: python

            # ---- admin.py file ----

            base = fancy_modeladmin('id')
            base.add_link('author', 'Our Authors',
                '{{obj.name}} (id={{obj.id}})')

            @admin.register(Book)
            class BookAdmin(base):
                pass

        The django admin change page for the Book class would have a column
        for "id" and another titled "Our Authors". The "Our Authors" column
        would have a link for each Author object referenced by "book.author".
        The link would go to the Author django admin change listing. The
        display of the link would be the name of the author with the id in
        brakcets, e.g. "Douglas Adams (id=42)"
        """
        global klass_count
        klass_count += 1
        fn_name = 'dyn_fn_%d' % klass_count
        cls.list_display.append(fn_name)

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

        setattr(cls, fn_name, _link)

    @classmethod
    def add_object(cls, attr, title='', display=''):
        """Adds a ``list_display`` attribute showing an object.  Supports
        double underscore attribute name dereferencing.

        :param attr:
            Name of the attribute to dereference from the corresponding
            object, i.e. what will be lined to.  This name supports double
            underscore object link referencing for ``models.ForeignKey``
            members.

        :param title:
            Title for the column of the django admin table.  If not given it
            defaults to a capitalized version of ``attr``

        :param display:
            What to display as the text for the link being shown.  If not
            given it defaults to the string representation of the object for
            the row: ``str(obj)``.  This parameter supports django templating,
            the context for which contains a dictionary key named "obj" with
            the value being the object for the row.
        """
        global klass_count
        klass_count += 1
        fn_name = 'dyn_fn_%d' % klass_count
        cls.list_display.append(fn_name)

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

        setattr(cls, fn_name, _ref)

    @classmethod
    def add_formatted_field(cls, field, format_string, title=''):
        """Adds a ``list_display`` attribute showing a field in the object
        using a python %formatted string.

        :param field:
            Name of the field in the object.

        :param format_string:
            A old-style (to remain python 2.x compatible) % string formatter
            with a single variable reference. The named ``field`` attribute
            will be passed to the formatter using the "%" operator. 

        :param title:
            Title for the column of the django admin table.  If not given it
            defaults to a capitalized version of ``field``
        """
        global klass_count
        klass_count += 1
        fn_name = 'dyn_fn_%d' % klass_count
        cls.list_display.append(fn_name)

        if not title:
            title = field.capitalize()

        # python scoping is a bit weird with default values, if it isn't
        # referenced the inner function won't see it, so assign it for use
        _format_string = format_string

        def _ref(self, obj):
            return _format_string % getattr(obj, field)
        _ref.short_description = title
        _ref.allow_tags = True
        _ref.admin_order_field = field

        setattr(cls, fn_name, _ref)



def fancy_modeladmin(*args):
    """Returns a new copy of a :class:`FancyModelAdmin` class (a class, not
    an instance!). This can then be inherited from when declaring a model
    admin class. The :class:`FancyModelAdmin` class has additional methods
    for managing the ``list_display`` attribute.

    :param ``*args``: [optional] any arguments given will be added to the
        ``list_display`` property using regular django ``list_display``
        functionality.

    This function is meant as a replacement for :func:`make_admin_obj_mixin`,
    it does everything the old one does with fewer bookkeeping needs for the
    user as well as adding functionality.

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


        base = fany_list_display_modeladmin()
        base.add_displays('id', 'name')
        base.add_obj_link('author', 'Our Authors',
            '{{obj.name}} (id={{obj.id}})')

        @admin.register(Book)
        class BookAdmin(base):
            list_display = ('name', 'show_author')


    A sample django admin page for "Book" would have the table:

    +----+---------------------------------+------------------------+
    | ID | Name                            | Our Authors            |
    +====+=================================+========================+
    |  1 | Hitchhikers Guide To The Galaxy | *Douglas Adams (id=1)* |
    +----+---------------------------------+------------------------+
    |  2 | War and Peace                   | *Tolstoy (id=2)*       |
    +----+---------------------------------+------------------------+
    |  3 | Dirk Gently                     | *Douglas Adams (id=1)* |
    +----+---------------------------------+------------------------+


    See :class:`FancyModelAdmin` for a full list of functionality
    provided by the returned base class.
    """
    global klass_count

    klass_count += 1
    name = 'DynamicAdminClass%d' % klass_count

    # clone the admin class
    klass = type(name, (FancyModelAdmin,), {})
    klass.list_display = []
    if len(args) > 0:
        klass.add_displays(*args)

    return klass
