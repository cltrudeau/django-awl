# awl.templatetags.awltags.py

from django import template

register = template.Library()

# ============================================================================

@register.filter
def getitem(dictionary, keyvar):
    """Custom django template filter that allows access to an item of a
    dictionary through the key contained in a template variable.  Example:

    .. code-block:: python

        context_data = {
            'data':{
                'foo':'bar',
            },
            'key':'foo',
        }

        template = Template('{% load awltags %}{{data|getitem:key}}')
        context = Context(context_data)
        result = template.render(context)

        >>> result
        'bar'

    .. note::
        Any KeyErrors are ignored and return an empty string
    """
    try:
        return dictionary[keyvar]
    except KeyError:
        return ''

# ----------------------------------------------------------------------------

@register.tag
def accessor(parser, token):
    """This template tag is used to do complex nested attribute accessing of
    an object.  The first parameter is the object being accessed, subsequent
    paramters are one of: 

    * a variable in the template context
    * a literal in the template context
    * either of the above surrounded in square brackets

    For each variable or literal parameter given a `getattr` is called on the
    object, chaining to the next parameter.  For any sqaure bracket enclosed
    items the access is done through a dictionary lookup.

    Example::

        {% accessor car where 'front_seat' [position] ['fabric'] %}

    The above would result in the following chain of commands:

    .. code-block:: python

        ref = getattr(car, where)
        ref = getattr(ref, 'front_seat')
        ref = ref[position]
        return ref['fabric']

    This tag also supports "as" syntax, putting the results into a template
    variable::

        {% accessor car 'interior' as foo %}
    """
    contents = token.split_contents()
    tag = contents[0]
    if len(contents) < 3:
        raise template.TemplateSyntaxError(('%s requires at least two '
            'arguments: object and one or more getattr parms') % tag)

    as_var = None
    if len(contents) >= 4:
        # check for "as" syntax
        if contents[-2] == 'as':
            as_var = contents[-1]
            contents = contents[:-2]

    return AccessorNode(contents[1], contents[2:], as_var)


class AccessorNode(template.Node):
    def __init__(self, obj_name, parms, as_var):
        self.obj_name = obj_name
        self.parms = parms
        self.as_var = as_var

    def render(self, context):
        try:
            ref = context[self.obj_name]
            for parm in self.parms:
                if parm[0] == '"' or parm[0] == "'":
                    # parm is a literal
                    ref = getattr(ref, parm[1:-1])
                elif parm[0] == '[':
                    # parm is a dictionary lookup
                    if parm[1] == '"' or parm[1] == "'":
                        # dict key is a literal
                        ref = ref[parm[2:-2]]
                    else:
                        # dict key is a template var
                        key = context[parm[1:-1]]
                        ref = ref[key]
                else:
                    # parm is a template var
                    attr = context[parm]
                    ref = getattr(ref, attr)

            if self.as_var:
                context[self.as_var] = ref
                return ''

            return ref
        except:
            # any lookup errors should result in empty
            if self.as_var:
                context[self.as_var] = ''

            return ''

# ----------------------------------------------------------------------------

@register.simple_tag
def nop(*args):
    """This tag does nothing. Useful for a comment without having to build a
    full comment block. All parameters are ignored.

    Example::

        {% nop 'this is a string' %}
    """
    return ''
