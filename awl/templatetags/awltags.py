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
    """
    return dictionary[keyvar]


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
    """
    contents = token.split_contents()
    tag = contents[0]
    if len(contents) < 3:
        raise template.TemplateSyntaxError(('%s requires at least two '
            'arguments: object and one or more getattr parms') % tag)

    return AccessorNode(contents[1], contents[2:])


class AccessorNode(template.Node):
    def __init__(self, obj_name, parms):
        self.obj_name = obj_name
        self.parms = parms

    def render(self, context):
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

        return ref
