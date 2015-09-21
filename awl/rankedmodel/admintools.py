# awl.rankedmodel.admin.py

from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

# =============================================================================
# RankedModel Helper Methods
# =============================================================================

def admin_link_move_up(obj, link_text='up'):
    """Returns a link to a view that moves the passed in object up in rank.

    :param obj:
        Object to move
    :param link_text:
        Text to display in the link.  Defaults to "up"
    :returns:
        HTML link code to view for moving the object
    """
    if obj.rank == 1:
        return ''

    content_type = ContentType.objects.get_for_model(obj)
    link = reverse('awl-rankedmodel-move', args=(content_type.id, obj.id, 
        obj.rank - 1))

    return '<a href="%s">%s</a>' % (link, link_text)


def admin_link_move_down(obj, link_text='down'):
    """Returns a link to a view that moves the passed in object down in rank.

    :param obj:
        Object to move
    :param link_text:
        Text to display in the link.  Defaults to "down"
    :returns:
        HTML link code to view for moving the object
    """
    if obj.rank == obj.grouped_filter().count():
        return ''

    content_type = ContentType.objects.get_for_model(obj)
    link = reverse('awl-rankedmodel-move', args=(content_type.id, obj.id, 
        obj.rank + 1))

    return '<a href="%s">%s</a>' % (link, link_text)
