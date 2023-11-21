from django.db import models

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
