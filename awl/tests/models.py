from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from awl.models import ValidatingMixin
from awl.rankedmodel.models import RankedModel

# ============================================================================
# Waelsteng Models
# ============================================================================

class Link(models.Model):
    url = models.CharField(max_length=80)
    text = models.CharField(max_length=80)


class Validator(ValidatingMixin, models.Model):
    counter = models.IntegerField(default=0)

    def full_clean(self):
        super(Validator, self).full_clean()
        self.counter += 1

# ============================================================================
# Admintools Models 
# ============================================================================

@python_2_unicode_compatible
class Nested(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return 'Nested(id=%s %s)' % (self.id, self.name)


@python_2_unicode_compatible
class Inner(models.Model):
    name = models.CharField(max_length=10)
    nested = models.ForeignKey(Nested)

    def __str__(self):
        return 'Inner(id=%s %s)' % (self.id, self.name)


class Outer(models.Model):
    name = models.CharField(max_length=10)
    inner = models.ForeignKey(Inner)

# ============================================================================
# RankedModel Models 

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
