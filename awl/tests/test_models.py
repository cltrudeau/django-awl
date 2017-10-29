# awl.tests.test_models.py
from django.test import TestCase

from awl.models import Counter, Lock, Choices, QuerySetChain
from awl.utils import refetch

# ============================================================================

class ModelsTest(TestCase):
    def test_counter(self):
        count = Counter.objects.create(name='foo')
        Counter.increment('foo')
        count = refetch(count)
        self.assertEqual(1, count.value)

    def test_lock(self):
        # not much to test here except that it doesn't blow up
        Lock.objects.create(name='foo')
        Lock.lock_until_commit('foo')

    def test_choices(self):
        class Colours(Choices):
            RED = 'r'
            LIGHT_ORANGE = 'o'
            BLUE = ('b', 'Blueish')

        class MoreColours(Colours):
            GREEN = 'g'

        # check the created values
        self.assertEqual(MoreColours.RED, 'r')
        self.assertEqual(MoreColours.LIGHT_ORANGE, 'o')
        self.assertEqual(MoreColours.BLUE, 'b')
        self.assertEqual(MoreColours.GREEN, 'g')

        # check conversion to django-style choices list
        l = list(MoreColours)
        self.assertEqual(len(l), 4)
        self.assertIn(('r', 'Red'), l)
        self.assertIn(('b', 'Blueish'), l)
        self.assertIn(('g', 'Green'), l)
        self.assertIn(('o', 'Light Orange'), l)

        # check gettr method
        self.assertEqual('Red', Colours.get_value('r'))
        self.assertEqual('Red', MoreColours.get_value('r'))

    def test_queryset_chain(self):
        # create some object to query
        from django.contrib.auth.models import User, Group
        User.objects.create(username='u1')
        User.objects.create(username='u2')
        User.objects.create(username='u3')
        Group.objects.create(name='g1')
        Group.objects.create(name='g2')

        # get 3 users and two groups
        users = User.objects.all()
        groups = Group.objects.all()

        # base case for chaining
        chain = QuerySetChain(users, groups)
        self.assertEqual(5, chain.count())

        # test slicing
        for item in chain[:3]:
            self.assertIsInstance(item, User)

        self.assertEqual(groups[0], chain[3])

        # trigger internal _clone(), make sure it doesn't blow up
        chain._clone()
