# awl.admintools.py
from django.core import urlresolvers
from django.template import Context, Template

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
    url = urlresolvers.reverse('admin:%s_%s_changelist' % (obj._meta.app_label,
        obj._meta.model_name))
    url += '?id__exact=%s' % obj.id

    text = str(obj)
    if display:
        text = display

    return '<a href="%s">%s</a>' % (url, text)


def make_admin_obj_mixin(name):
    """This method dynamically creates mixin to be used with your 
    :class:`ModelAdmin` classes that provides methods to display links to
    related objects.

    :param name:
        Each usage of the mixin must be given a unique name for the mixin class
        being created
    :returns:
        Dynamically created mixin class

    The created class will have a single method:

    .. code-block:: python

        add_obj_link(funcname, attr, [title, display])

    :param funcname:
        Name of the function to be added to the mixin.  This would normally
        correspond to an item in the :class:`ModelAdmin` class's
        ``list_display`` tuple
    :param attr:
        Name of the attribute belonging to the object instance of the model
        that the :class:`ModelAdmin` repsresents.  This essentially identifies
        what will be linked to
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

        # models file

        class Inner(models.Model):
            name = models.CharField(max_length=10)


        class Outer(models.Model):
            name = models.CharField(max_length=10)
            inner = models.ForeignKey(Inner)


        # admin file
        @admin.register(Inner)
        class InnerAdmin(admin.ModelAdmin):
            list_display = ('name', )



        base = make_admin_obj_mixin('OuterMixin')
        base.add_obj_link('show_inner', 'inner', 'My Inner',
            'Inner.id={{obj.id}}')

        @admin.register(Outer)
        class OuterAdmin(admin.ModelAdmin):
            list_display = ('name', 'show_inner')


    A sample django admin page for "Outer" would have the table:

    +---------+-------------+
    | Name    | My Inner    |
    +=========+=============+
    | One     | Inner.id=1  |
    +---------+-------------+
    | Two     | Inner.id=2  |
    +---------+-------------+
    | Three   | Inner.id=3  |
    +---------+-------------+

    Each of the items in the "My Inner" column would be a link to the django
    admin change list for the "Inner" object with a filter set to show just
    the object that was clicked.
    """
    @classmethod
    def add_obj_link(cls, funcname, attr, title='', display=''):
        if not title:
            title = attr.capitalize()

        # python scoping is a bit weird with default values, if it isn't
        # reference the inner function won't see it, so assign it for use
        _display = display

        def _link(self, obj):
            # handle '__' referencing like in QuerySets
            fields = attr.split('__')
            field_obj = getattr(obj, fields[0])

            for field in fields[1:]:
                # keep going down the reference tree
                field_obj = getattr(field_obj, field)

            link_name = ''
            if not _display:
                link_name = str(field_obj)
            else:
                template = Template(_display)
                context = Context({'obj':obj})
                link_name = template.render(context)

            return admin_obj_link(field_obj, link_name)
        _link.short_description = title
        _link.allow_tags = True
        _link.admin_order_field = attr

        setattr(cls, funcname, _link)

    klass = type(name, (), {})
    klass.add_obj_link = add_obj_link
    return klass
