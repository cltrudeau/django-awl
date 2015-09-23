# awl.rankedmodel.models.py
from django.db import models, transaction

# ============================================================================

class RankedModel(models.Model):
    """Abstract model used to have all the inheritors ordered in the database
    by this model's ``rank`` field.   Ranks can either be across all instances
    of the inheriting model, or in a series of groups.  See
    :class:`RankedModel.group_filter` for details on implementing grouping.

    The ``rank`` field can be set and saved like any other field.  The
    overridden :class:`RankedModel.save` method maintains rank integrity.
    The order is maintained
    but it is not guaranteed that there are not gaps in the rank count -- for
    simplicity re-ordering is not done on deletion.  If empty slots are a
    concern, use :class:`RankedModel.repack`.

    .. warning::

        Due to the use of the overridden ``save()`` for integrity caution must
        be employed when dealing with any ``update()`` calls or raw SQL as
        these will not call the ``save()`` method.

    Two admin helper functions are provided so you can do rank re-ording in
    the django admin.  To use the functions, add columns to your admin
    instances of the inheriting class::

        from awl.admin import admin_link_move_up, admin_link_move_down

        @admin.register(Favourites)
        class FavouritesAdmin(admin.ModelAdmin):
            list_display = ('name', 'rank', 'move_up', 'move_down')

            def move_up(self, obj):
                return admin_link_move_up(obj)
            move_up.allow_tags = True
            move_up.short_description = 'Move Up Rank'

            def move_down(self, obj):
                return admin_link_move_down(obj)
            move_down.allow_tags = True
            move_down.short_description = 'Move Up Rank'

    :param rank:
        Ranked order of object
    """
    rank = models.PositiveSmallIntegerField(db_index=True)

    class Meta:
        abstract = True
        ordering = ['rank']

    def __init__(self, *args, **kwargs):
        super(RankedModel, self).__init__(*args, **kwargs)
        self._rank_at_load = self.rank

    def _process_new_rank_obj(self):
        # no id yet, this is the first time this object has been saved
        rank = getattr(self, 'rank', None)
        items = self.grouped_filter().order_by(
            'rank').select_for_update()
        count = items.count()
        if count == 0:
            self.rank = 1
        else:
            if not rank or rank > count + 1:
                # rank not set yet, or was set larger than largest item
                self.rank = count + 1
            elif rank < 1:
                self.rank = 1

            # count >= 1, need to move everybody else

            # rank was set to a specific value, need to re-order
            # everything that comes after it in the list
            for item in items[self.rank - 1:]:
                item.rank +=1
                item._rank_at_load = item.rank
                item.save(rerank=False)

        self._rank_at_load = self.rank

    def _process_moved_rank_obj(self):
        # rank changed, re-order it
        items = self.grouped_filter().order_by('rank').select_for_update()
        count = items.count()

        # check bounds on new rank
        if self.rank < 1:
            self.rank = 1
        elif self.rank > count:
            self.rank = count

        if self.rank < self._rank_at_load:
            # rank moved down
            start = self.rank - 1
            end = self._rank_at_load - 1
            delta = 1
        else:
            # rank moved up
            start = self._rank_at_load
            end = self.rank
            delta = -1

        for item in items[start:end]:
            item.rank += delta
            item._rank_at_load = item.rank
            item.save(rerank=False)

    @transaction.atomic
    def save(self, *args, **kwargs):
        """Overridden method that handles that re-ranking of objects and the
        integrity of the ``rank`` field.

        :param rerank:
            Added parameter, if True will rerank other objects based on the
            change in this save.  Defaults to True.  
        """
        rerank = kwargs.pop('rerank', True)
        if rerank:
            if not self.id:
                self._process_new_rank_obj()
            elif self.rank == self._rank_at_load:
                # nothing changed
                pass
            else:
                self._process_moved_rank_obj()

        super(RankedModel, self).save(*args, **kwargs)

    def grouped_filter(self):
        """This method should be overridden in order to allow groupings of
        ``RankModel`` objects.  The default is there is a single group which
        are all instances of the inheriting class.  

        An example with a grouped model would be::

            class Grouped(RankedModel):
                group_number = models.IntegerField()

                def grouped_filter(self):
                    return Grouped.objects.filter(
                        group_number=self.group_number)

        :returns:
            :class:`QuerySet` of ``RankedModel`` objects that are in the same
            group.
        """
        return self.__class__.objects.all()

    def repack(self):
        """Removes any blank ranks in the order."""
        items = self.grouped_filter().order_by('rank').select_for_update()
        for count, item in enumerate(items):
            item.rank = count + 1
            item.save(rerank=False)
