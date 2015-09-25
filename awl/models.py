from django.db import models, transaction

# ============================================================================
# Abstract Models
# ============================================================================

class TimeTrackModel(models.Model):
    """Abstract model with auto-updating create & update timestamp fields.

    :param created:
        Date/time when the model was created
    :param updated:
        Date/time when the model was last updated
    """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ValidatingMixin(models.Model):
    """Include this mixin to force model validation to happen on each
    ``save`` call.
    """
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.full_clean()
        super(ValidatingMixin, self).save(*args, **kwargs)

# ============================================================================
# Concrete Models
# ============================================================================

class Counter(TimeTrackModel):
    """A named counter in the database with atomic update."""
    name = models.CharField(max_length=30)
    value = models.BigIntegerField(default=0)

    @classmethod
    def increment(cls, name):
        """Call this method to increment the named counter.  This is atomic on
        the database.

        :param name:
            Name for a previously created ``Counter`` object 
        """
        with transaction.atomic():
            counter = Counter.objects.select_for_update().get(name=name)
            counter.value += 1
            counter.save()

        return counter.value


class Lock(TimeTrackModel):
    """Implements a simple global locking mechanism across database accessors
    by using the ``select_for_update()`` feature.  Example:

    .. code-block:: python

        # run once, or use a fixture
        Lock.objects.create(name='everything')

        # views.py
        def something(request):
            Lock.lock_until_commit('everything')

    """
    name = models.CharField(max_length=30)

    @classmethod
    def lock_until_commit(cls, name):
        """Grabs this lock and holds it (using ``select_for_update()``) until
        the next commit is done.

        :param name:
            Name for a previously created ``Lock`` object 
        """
        Lock.objects.select_for_update().get(name=name)
