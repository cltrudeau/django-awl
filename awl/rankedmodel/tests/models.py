from django.contrib import admin
from django.db import models

from awl.rankedmodel.admintools import admin_link_move_up, admin_link_move_down
from awl.rankedmodel.models import RankedModel

# ============================================================================
# Models used by tests

class Alone(RankedModel):
    name = models.CharField(max_length=1)

    def __init__(self, *args, **kwargs):
        # ignore fake group entry to make the constructors the same for both
        # test models
        kwargs.pop('group', None)
        super(Alone, self).__init__(*args, **kwargs)


class Grouped(RankedModel):
    group = models.CharField(max_length=1)
    name = models.CharField(max_length=1)

    def grouped_filter(self):
        return Grouped.objects.filter(group=self.group)

# ============================================================================
# Admin Models for tests

class RankAdmin(admin.ModelAdmin):
    list_display = ('name', 'move_up', 'move_down')

    def move_up(self, obj):
        return admin_link_move_up(obj)
    move_up.allow_tags = True
    move_up.short_description = 'Move Up Rank'

    def move_down(self, obj):
        return admin_link_move_down(obj)
    move_down.allow_tags = True
    move_down.short_description = 'Move Up Rank'
