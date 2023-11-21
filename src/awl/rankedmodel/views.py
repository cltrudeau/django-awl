# awl.rankedmodel.views.py

from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

# ============================================================================

@staff_member_required
def move(request, content_type_id, obj_id, rank):
    """View to be used in the django admin for changing a :class:`RankedModel`
    object's rank.  See :func:`admin_link_move_up` and
    :func:`admin_link_move_down` for helper functions to incoroprate in your
    admin models.

    Upon completion this view sends the caller back to the referring page.

    :param content_type_id:
        ``ContentType`` id of object being moved
    :param obj_id:
        ID of object being moved
    :param rank:
        New rank of the object
    """
    content_type = ContentType.objects.get_for_id(content_type_id)
    obj = get_object_or_404(content_type.model_class(), id=obj_id)
    obj.rank = int(rank)
    obj.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])
