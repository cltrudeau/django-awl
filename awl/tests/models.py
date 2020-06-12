from django.db import models

from awl.absmodels import ValidatingMixin
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

class Author(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return 'Author(id=%s %s)' % (self.id, self.name)


class Book(models.Model):
    name = models.CharField(max_length=20)
    author = models.ForeignKey(Author, null=True, blank=True,
        on_delete=models.CASCADE)

    def __str__(self):
        return 'Book(id=%s %s)' % (self.id, self.name)

    @property
    def classname(self):
        return 'Book'


class Chapter(models.Model):
    name = models.CharField(max_length=20)
    book = models.ForeignKey(Book, null=True, blank=True,
        on_delete=models.CASCADE)

# ----------------------------------------------------------------------------

class VehicleMake(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return 'VehicleMake(id=%s %s)' % (self.id, self.name)


class VehicleModel(models.Model):
    name = models.CharField(max_length=20)
    year = models.PositiveIntegerField(blank=True, null=True)
    vehiclemake = models.ForeignKey(VehicleMake, null=True, blank=True,
        on_delete=models.CASCADE)

    def __str__(self):
        return 'VehicleModel(id=%s %s)' % (self.id, self.name)

    @property
    def fullname(self):
        return '%s %s' % (self.vehiclemake.name, self.name)


class Driver(models.Model):
    name = models.CharField(max_length=20)
    vehiclemodel = models.ForeignKey(VehicleModel, null=True, blank=True,
        on_delete=models.CASCADE)
    rating = models.FloatField(null=True)


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

# ============================================================================
# get_field_names() models

class Address(models.Model):
    address_info = models.CharField(max_length=30)


class Course(models.Model):
    course_name = models.CharField(max_length=30)


class Person(models.Model):
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=30)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course)
    best_friend = models.OneToOneField('Person', on_delete=models.CASCADE)


class Building(models.Model):
    superintendent = models.ForeignKey(Person, on_delete=models.CASCADE)


