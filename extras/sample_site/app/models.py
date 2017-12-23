from django.db import models

class Nested(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return 'Nested(id=%s %s)' % (self.id, self.name)


class Inner(models.Model):
    name = models.CharField(max_length=10)
    nested = models.ForeignKey(Nested, on_delete=models.CASCADE)

    def __str__(self):
        return 'Inner(id=%s %s)' % (self.id, self.name)


class Outer(models.Model):
    name = models.CharField(max_length=10)
    inner = models.ForeignKey(Inner, on_delete=models.CASCADE)

    def __str__(self):
        return 'Outer(id=%s %s)' % (self.id, self.name)
