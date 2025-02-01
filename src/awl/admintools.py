# awl.admintools.py
from warnings import warn

from django.contrib.admin import ModelAdmin
from django.contrib.admin.utils import lookup_field
from django.template import Context, Template
from django.urls import reverse
from django.utils.html import format_html

from awl.utils import get_obj_attr

# ============================================================================
# Admin Object Getters
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


def _obj_display(obj, display='', extra_context={}):
    """Returns string representation of an object, either the default or based
    on the display template passed in.
    """
    result = ''
    if not display:
        result = str(obj)
    else:
        template = Template(display)

        context_dict = {
            'obj':obj,
        }
        context_dict.update(extra_context)
        context = Context(context_dict)
        result = template.render(context)

    return result

# ============================================================================
# Old Mixin Maker (Deprecated)
# ============================================================================

def make_admin_obj_mixin(name):
    """**DEPRECATED** Use :func:`fancy_modeladmin` instead.

    This method dynamically creates a mixin to be used with your 
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
            title = attr.replace('_', ' ').capitalize()

        def _link(self, obj):
            field_obj = admin_obj_attr(obj, attr)
            if not field_obj:
                return ''

            nonlocal display
            text = _obj_display(field_obj, display)
            return admin_obj_link(field_obj, text)
        _link.short_description = title
        _link.admin_order_field = attr

        setattr(cls, funcname, _link)

    @classmethod
    def add_obj_ref(cls, funcname, attr, title='', display=''):
        if not title:
            title = attr.replace('_', ' ').capitalize()

        def _ref(self, obj):
            field_obj = admin_obj_attr(obj, attr)
            if not field_obj:
                return ''

            nonlocal display
            return _obj_display(field_obj, display)
        _ref.short_description = title
        _ref.admin_order_field = attr

        setattr(cls, funcname, _ref)

    warn('Replaced by FancyModelAdmin class', DeprecationWarning)
    klass = type(name, (), {})
    klass.add_obj_link = add_obj_link
    klass.add_obj_ref = add_obj_ref
    return klass

# ============================================================================
# Newer Admin Object Mechanism
# ============================================================================

klass_count = 0

class FancyModelAdmin(ModelAdmin):
    """A replacement for :class:`admin.ModelAdmin` which provides additional
    methods for improving how the ``list_display`` attribute works. 

    This class should not be instantiated directly, instead call 
    :func:`fancy_modeladmin`.
    """
    list_display = []

    @classmethod
    def _new_func_name(cls):
        global klass_count
        klass_count += 1
        fn_name = 'dyn_fn_%d' % klass_count
        cls.list_display.append(fn_name)
        return fn_name

    @classmethod
    def add_displays(cls, *args):
        """Each arg is added to the ``list_display`` property without any
        extra wrappers. Can be used to reference callable methods."""
        for arg in args:
            cls.list_display.append(arg)

    @classmethod
    def add_display(cls, attr, title='', empty=''):
        """**DEPRECATED!** Use :func:`FancyModelAdmin.add_field`

        Adds a column that displays a field in the object.

        :param attr:
            Name of the attribute to add to the display

        :param title:
            Title for the column of the django admin table.  If not given it
            defaults to a capitalized version of ``attr``

        :param empty:
            What to display instead if there is no value. Defaults to empty
            string. Supports HTML formatting, i.e. could set it to 
            '<i>undefined</i>'.
        """
        warn('Deprecated, use add_field() instead', DeprecationWarning)
        cls.add_field(attr, title, empty)

    @classmethod
    def add_field(cls, attr, title='', empty=''):
        """Adds a column that shows a field in the object. 

        Note that this cannot be used to add a callable, it only works with
        attributes on the object.

        :param attr:
            Attribute of the field to be added

        :param title:
            Title for the column of the django admin table.  If not given it
            defaults to a capitalized version of ``attr``

        :param empty:
            What to display instead if there is no value. Defaults to empty
            string. Supports HTML formatting, i.e. could set it to 
            '<i>undefined</i>'.
        """
        # add_field()
        fn_name = cls._new_func_name()

        if not title:
            title = attr.replace('_', ' ').capitalize()

        def _ref(self, obj):
            # use the django mechanism for field value lookup
            _, _, value = lookup_field(attr, obj, cls)
            if value:
                return value

            return format_html(empty)
        _ref.short_description = title
        _ref.admin_order_field = attr

        setattr(cls, fn_name, _ref)

    @classmethod
    def add_link(cls, attr, title='', display='', empty=''):
        """Adds a column that contains a link to another object's Django 
        Admin page. Used with Foreign Keys and OneToOneFields that are fields
        on this object (forward links).

        The link goes to the corresponding Django Admin change list page,
        filtered to the object clicked. 

        Supports double underscore attribute name dereferencing.

        :param attr:
            Name of the attribute to dereference from the corresponding
            object, i.e. what will be linked to.  This name supports double
            underscore object link referencing for ``models.ForeignKey``
            members.

        :param title:
            Title for the column of the django admin table.  If not given it
            defaults to a capitalized version of ``attr``

        :param display:
            What to display as the text for the link being shown.  If not
            given it defaults to the string representation of the linked
            object.  This parameter supports django templating, the context
            for which contains a dictionary key named "obj" with the value
            being the linked object for the row.

        :param empty:
            Value to display if there is no link for the object. Defaults to
            an empty string. Can contain HTML.

        Example usage:

        .. code-block:: python

            # ---- models.py file ----

            class Account(models.Model):
                ...

            class Client(models.Model):
                account = models.ForeignKey(Account)

            # ---- admin.py file ----

            base = fancy_modeladmin('id')
            base.add_link('account', 'Account', '{{obj}}')

            @admin.register(Client)
            class ClientAdmin(base):
                pass

        The above example causes the Book class change list page to have a
        column for "id" and another titled "Account". The "Account"
        column will have a link to the change list page for the Account object
        filtered by Book that was clicked.  The
        display of the link would be the name display string of the
        corresponding Account object.
        """
        # add_link()
        fn_name = cls._new_func_name()

        if not title:
            title = attr.replace('_', ' ').capitalize()

        def _link(self, obj):
            nonlocal display, empty

            field_obj = admin_obj_attr(obj, attr)
            if not field_obj:
                return format_html(empty)

            text = _obj_display(field_obj, display)
            return admin_obj_link(field_obj, text)
        _link.short_description = title
        _link.admin_order_field = attr

        setattr(cls, fn_name, _link)

    @classmethod
    def add_m2m_link(cls, attr, title='', display='', empty=''):
        """Adds a column that contains a link to an object change list
        filtered to contain all of the objects associated through a
        many-to-many relationship on this object.

        Note that the filtering on the related object is done through an "in"
        query of all the ids of the related many-to-many object. This feature
        should not be used for large relationships.

        :param attr:
            Name of the many-to-many attribute on the object being referenced.

        :param title:
            Title for the column of the Django Admin table.  If not given it
            defaults to a capitalized version of ``attr``

        :param display:
            What to display as the text for the link being shown.  If not
            given it defaults to a string showing the number of related items
            and the title variable.  This parameter supports Django
            templating. The context for the template includes a key named
            "row", which is the object for the row, a key named "count",
            which is the number of related items, and a key named
            "title" which is the title string passed in.

        :param empty:
            Value to display if there is are no relationships associated with 
            this object. Defaults to an empty string. Can contain HTML.

        Example usage:

        .. code-block:: python

            # ---- models.py file ----

            class Book(models.Model):
                publishers = models.ManyToManyField(Publisher)

            # ---- admin.py file ----

            base = fancy_modeladmin('id')
            base.add_link('publishers', 'Published By', 
                '{{obj.count}} Publishers')

            @admin.register(Book)
            class BookAdmin(base):
                pass

        The above example would produce a Django Admin change list for the
        Book class would have a column for "id" and another titled
        "Published By". The "Published By" column would have a link to the 
        Publisher change listing, filtered for the each Book row.

        The link would say "# Publishers", where # is the number of Publisher 
        objects related with the book. 
        """
        # add_m2m_link()
        fn_name = cls._new_func_name()

        if not title:
            title = attr.replace('_', ' ').capitalize()

        def _link(self, row):
            nonlocal display, empty
            m2m = getattr(row, attr, None)
            count = m2m.count()
            if count == 0:
                return format_html(empty)

            # get the url for the change list for this object
            related_class = m2m.model
            all_ids = [str(x) for x in m2m.values_list('id', flat=True)]
            all_ids = ','.join(all_ids)

            url = reverse('admin:%s_%s_changelist' % (
                related_class._meta.app_label, related_class._meta.model_name))
            url += f'?id__in={all_ids}'

            if not display:
                display = '{{count}} {{title}}'

            extra_context = {
                'count':count,
                'title':title,
                'row':row,
            }

            text = _obj_display(m2m, display, extra_context)
            return format_html('<a href="{}">{}</a>', url, text)
        _link.short_description = title

        setattr(cls, fn_name, _link)

    @classmethod
    def add_fk_link(cls, set_name, related_class, fk_attr, title='', 
            display='', empty=''):
        """Adds a column containing a link to an object that has a Foreign Key
        that points to this object (backward referencing). 

        The link takes the user to the Django Admin change list, filtered for
        the object that was clicked to get there.

        :param set_name:
            Name of the attribute on the row object that is the foreign key
            set. For example "grade_set" on a Student object that is
            associated with a Grade object through Grade's FK on Student.

        :param related_class:
            The class that has the foreign key to the row object.  This is
            used to find the corresponding admin change listing page.

        :param fk_attr:
            The name of the attribute on the related object that is a foreign
            key pointing to this row object. Used to create the query string
            that filters the change listing.

        :param title:
            Title for the column header. If not given, the related_class is
            used.

        :param display:
            What to display as the text for the link being shown.  If not
            given it defaults to a string showing the number of related items
            and the title variable.  This parameter supports django
            templating. The context for the template includes a key named
            "row", which is the object for the row, a key named "count",
            which is the number of items in the named set, and a key named
            "title" which is the title string passed in.

        :param empty:
            Value to display if there are no related objects. Supports HTML.

        Example usage:

        .. code-block:: python

            # ---- admin.py file ----

            base = fancy_modeladmin('id')
            base.add_fk_link('grade_set', Grade, '{{obj.count}} Grades')

            @admin.register(Student)
            class StudentAdmin(base):
                pass

        The above example produces a Django Admin change list for the Student
        class that has a "id" and "Grades" columns.  The "Grades" column
        contains a link to the Grade class's change listing, filtered for the
        Student row.

        The link is displayed as "# Grades", where # is the number of Grade 
        objects associated with the Student row. In this case, the template
        passed in the same as the default and wouldn't be necessary.
        """
        # add_fk_link()
        fn_name = cls._new_func_name()

        if not title:
            title = related_class._meta.model_name.capitalize()

        def _link(self, row):
            nonlocal display, empty
            set_object = getattr(row, set_name, None)
            count = set_object.count()
            if count == 0:
                return format_html(empty)

            # get the url for the change list for this object
            url = reverse('admin:%s_%s_changelist' % (
                related_class._meta.app_label, related_class._meta.model_name))
            url += '?%s__id=%s' % (fk_attr, row.id)

            if not display:
                display = '{{count}} {{title}}'

            extra_context = {
                'count':count,
                'title':title,
                'row':row,
            }

            text = _obj_display(set_object, display, extra_context)
            return format_html('<a href="{}">{}</a>', url, text)
        _link.short_description = title

        setattr(cls, fn_name, _link)

    @classmethod
    def add_object(cls, attr, title='', display='', empty=''):
        """Adds a column showing the contents of a field as an object. Similar
        to :func:`FancyModelAdmin.add_link`, but as plain text. Supports
        double underscore attribute name dereferencing.

        :param attr:
            Name of the attribute to dereference from the corresponding
            row.  This name supports double underscore object link referencing
            for ``models.ForeignKey`` members.

        :param title:
            Title for the column of the django admin table.  If not given it
            defaults to a capitalized version of ``attr``

        :param display:
            What to display as the text for the link being shown.  If not
            given it defaults to the string representation of the related
            object.  This parameter supports django templating, the context
            for which contains a dictionary key named "obj" with the value
            being the referenced object that is an attribute of the row
            object.

        :param empty:
            Value to display if there is no object for this row. Supports
            HTML.
        """
        fn_name = cls._new_func_name()

        if not title:
            title = attr.replace('_', ' ').capitalize()

        def _ref(self, obj):
            nonlocal empty
            field_obj = admin_obj_attr(obj, attr)
            if not field_obj:
                return format_html(empty)

            nonlocal display
            return _obj_display(field_obj, display)
        _ref.short_description = title
        _ref.admin_order_field = attr

        setattr(cls, fn_name, _ref)

    @classmethod
    def add_formatted_field(cls, field, format_string, title=''):
        """Adds a column showing a field in the object using a python 
        %formatted string.

        :param field:
            Name of the field in the object.

        :param format_string:
            A C-style % string formatter with a single variable reference. The
            named ``field`` attribute will be passed to the formatter using
            the "%" operator. 

        :param title:
            Title for the column of the django admin table.  If not given it
            defaults to a capitalized version of ``field``
        """
        fn_name = cls._new_func_name()

        if not title:
            title = field.replace('_', ' ').capitalize()

        def _ref(self, obj):
            nonlocal format_string
            return format_string % getattr(obj, field)
        _ref.short_description = title
        _ref.admin_order_field = field

        setattr(cls, fn_name, _ref)

    @classmethod
    def add_templated_field(cls, field, template, title=''):
        """Adds a column based on a field that is rendered using a Django
        template.

        :param field:
            Name of the field in the object.

        :param template:
            A string containing a Django template. Context is passed in with
            the keys "row" and "field", for the row object and field being
            displayed, respectively.

        :param title:
            Title for the column of the django admin table.  If not given it
            defaults to a capitalized version of ``field``
        """
        fn_name = cls._new_func_name()

        if not title:
            title = field.replace('_', ' ').capitalize()

        def _ref(self, row):
            nonlocal template
            template_object = Template(template)

            context_dict = {
                'row':row,
                'field':getattr(row, field),
            }
            context = Context(context_dict)
            result = template_object.render(context)
            return result
        _ref.short_description = title
        _ref.admin_order_field = field

        setattr(cls, fn_name, _ref)


def fancy_modeladmin(*args):
    """Returns a new copy of a :class:`FancyModelAdmin` class (a class, not
    an instance!). This can then be inherited from when declaring a model
    admin class. The :class:`FancyModelAdmin` class has additional methods
    for managing the ``list_display`` attribute.

    :param ``*args``: [optional] any arguments given will be added to the
        ``list_display`` property using regular Django ``list_display``
        functionality.

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


        base = fancy_modeladmin()
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
