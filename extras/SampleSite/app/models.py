from django.db import models

class Writer(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return 'Writer(id=%s %s)' % (self.id, self.name)


class Station(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return 'Station(id=%s %s)' % (self.id, self.name)


class Show(models.Model):
    title = models.CharField(max_length=50)
    writer = models.ForeignKey(Writer, on_delete=models.CASCADE, null=True,
        blank=True)
    stations = models.ManyToManyField(Station)

    def __str__(self):
        return 'Show(id=%s %s)' % (self.id, self.title)


class Episode(models.Model):
    name = models.CharField(max_length=50)
    show = models.ForeignKey(Show, on_delete=models.CASCADE, null=True,
        blank=True)

    def __str__(self):
        if self.show is None:
            return 'Episode(id=%s --%s)' % (self.id, self.name)

        return 'Episode(id=%s %s:%s)' % (self.id, self.show.title, self.name)
