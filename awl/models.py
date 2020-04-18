from itertools import islice, chain
from django.db import models, transaction

from awl.absmodels import TimeTrackModel

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

# ============================================================================
# Misc
# ============================================================================

# Choices
#
# idea borrowed, modified then converted to python 3 from:
#  http://tomforb.es
#      /using-python-metaclasses-to-make-awesome-django-model-field-choices

class _ChoicesType(type):
    # Metaclass for the Choices object
    #

    def __new__(metacls, classname, bases, namespace, **kwds):
        # create the class
        cls = type.__new__(metacls, classname, bases, namespace, **kwds)

        if classname == 'Choices':
            # this is the abstract base class, do nothing more
            return cls

        if not hasattr(cls, '_choices_hash'):
            # define a has to contain our choices only if a parent hasn't done
            # it already -- this allows grandchildren of Choices to override
            # their parent's values
            cls._choices_hash = {}

        # values defined in the class (not in parent) are defined in __dict__,
        # loop through them and update _choices_hash; this will override
        # anything defined in a parent 
        for name in cls.__dict__.keys():
            value = getattr(cls, name)
            if name[0] == '_' or hasattr(value, '__call__') :
                # attribute is hidden or callable, ignore it

                # coverage is doing something funky with just a "continue"
                # here, ugly hack to force it to recognize the code
                x = 1
                x += 1
                continue

            if isinstance(value, tuple) and len(value) > 1:
                # value is a tuple, override the value to be just the first
                # part and set the content hash to be the second part
                setattr(cls, name, value[0])
                cls._choices_hash[value[0]] = value[1]
            else:
                # value is not a tuple, create a default choice name based on
                # the class attribute
                pieces = [x.capitalize() for x in name.split('_')]
                cls._choices_hash[value] = ' '.join(pieces)

        return cls

    def __iter__(cls):
        for name, value in cls._choices_hash.items():
            yield (name, value)


class Choices(metaclass=_ChoicesType):
    """
    .. note::
        Django 3.0 added `Enumeration Types <https://docs.djangoproject.com/en/3.0/ref/models/fields/#enumeration-types>`_
        which solves the same problem as this class. You should probably use
        it instead.

    A tuple of tuples pattern of ((id1, string1), (id2, string2)...)  is
    common in django for choices fields, etc.  This object inspects its own
    members (i.e. the inheritors) and produces the corresponding tuples.

    .. code-block:: python

        class Colours(Choices):
            RED = 'r'
            LIGHT_BLUE = 'b'

        >> Colours.RED
        'r'
        >> list(Colours)
        [('r', 'Red'), ('b', 'Light Blue')]

    A member value can also be a tuple to override the default string

    .. code-block:: python

        class Colours(Choices):
            RED = 'r'
            BLUE = 'b', 'Blueish'

        >> list(Colours)
        [('r', 'Red'), ('b', 'Blueish')]


    A inheriting class can also add or override members.

    .. code-block:: python

        class Colours(Choices):
            RED = 'r'
            BLUE = 'b'

        class MoreColours(Colours):
            GREEN = 'g'
            BLUE = 'b', 'Even More Blue'

        >> list(Colours)
        [('r', 'Red'), ('b', 'Even More Blue'), ('g', 'Green')]
    """
    @classmethod
    def get_value(cls, key):
        return cls._choices_hash[key]

# ----------------------------------------------------------------------------

# QuerySetChain
#
# borrowed and modified from:
#   http://stackoverflow.com/questions/431628/
#   by: http://stackoverflow.com/users/15770/akaihola
class QuerySetChain:
    """
    Chains together multiple querysets (possibly of different models) and 
    behaves as one queryset.  Supports minimal methods needed for use with
    django.core.paginator.  Does not support re-ordering or re-filtering
    across the set.

    .. code-block:: python

        q1 = Thing.objects.filter(foo)
        q2 = Stuff.objects.filter(bar)
        qsc = QuerySetChain(q1, q2)
    """

    def __init__(self, *subquerysets):
        self.querysets = subquerysets

    def count(self):
        """
        Performs a .count() for all subquerysets and returns the number of
        records as an integer.
        """
        return sum(qs.count() for qs in self.querysets)

    def _clone(self):
        "Returns a clone of this queryset chain"
        return self.__class__(*self.querysets)

    def _all(self):
        "Iterates records in all subquerysets"
        return chain(*self.querysets)

    def __getitem__(self, index):
        """
        Retrieves an item or slice from the chained set of results from all
        subquerysets.
        """
        if type(index) is slice:
            return list(islice(self._all(), index.start, index.stop, 
                index.step or 1))
        else:
            return next(islice(self._all(), index, index+1))
