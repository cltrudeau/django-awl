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
