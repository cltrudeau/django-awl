# awl.rankedmodel.admin.py

from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe

# =============================================================================
# RankedModel Helper Methods
# =============================================================================

def admin_link_move_up(obj, link_text='↑'):
    """Returns a link to a view that moves the passed in object up in rank.

    :param obj:
        Object to move
    :param link_text:
        Text to display in the link.  Defaults to "↑"
    :returns:
        HTML link code to view for moving the object
    """
    if obj.rank == 1:
        return ''

    content_type = ContentType.objects.get_for_model(obj)
    link = reverse('awl-rankedmodel-move', args=(content_type.id, obj.id, 
        obj.rank - 1))

    return format_html('<a href="{}">{}</a>', link, link_text)


def admin_link_move_down(obj, link_text='↓'):
    """Returns a link to a view that moves the passed in object down in rank.

    :param obj:
        Object to move
    :param link_text:
        Text to display in the link.  Defaults to "↓"
    :returns:
        HTML link code to view for moving the object
    """
    if obj.rank == obj.grouped_filter().count():
        return ''

    content_type = ContentType.objects.get_for_model(obj)
    link = reverse('awl-rankedmodel-move', args=(content_type.id, obj.id, 
        obj.rank + 1))

    return format_html('<a href="{}">{}</a>', link, link_text)


def admin_move_links(obj, up_text='↑', down_text='↓'):
    """Returns a formatted column with up to two links in it for moving the
    passed in object up or down in rank.

    :param obj:
        Object to move
    :param up_text:
        Text to display in the up link.  Defaults to "↑"
    :param down_text:
        Text to display in down the link.  Defaults to "↓"
    :returns:
        HTML link code to view for moving the object
    """
    show_up = True
    show_down = True

    if obj.rank == 1:
        show_up = False

    if obj.rank == obj.grouped_filter().count():
        show_down = False

    html = f'<span style="width:{len(up_text)+1}ex; display:inline-block">'
    if show_up:
        content_type = ContentType.objects.get_for_model(obj)
        link = reverse('awl-rankedmodel-move', args=(content_type.id, obj.id, 
            obj.rank - 1))
        html += f'<a href="{link}">{up_text}</a>'
    else:
        html += '&nbsp;'

    html += '</span>&nbsp;' + \
        f'<span style="width:{len(down_text)+1}ex; display:inline-block">'
    if show_down:
        content_type = ContentType.objects.get_for_model(obj)
        link = reverse('awl-rankedmodel-move', 
            args=(content_type.id, obj.id, obj.rank + 1))
        html += f'<a href="{link}">{down_text}</a>'

    html += '</span>'

    return mark_safe(html)
