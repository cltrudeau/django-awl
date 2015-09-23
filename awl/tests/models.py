from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# ============================================================================
# Waelsteng Models
# ============================================================================

class Link(models.Model):
    url = models.CharField(max_length=80)
    text = models.CharField(max_length=80)

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
