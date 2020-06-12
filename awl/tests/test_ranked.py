import re

from django.test import TestCase

from awl.tests.admin import RankAdmin
from awl.tests.models import Alone, Grouped

from awl.waelsteng import AdminToolsMixin
from awl.utils import refetch

# ============================================================================

class RankModelBase(TestCase, AdminToolsMixin):
    def assertValues(self, objs, expected):
        names = [o.name for o in objs]
        compare = expected.split(',')
        self.assertEqual(compare, names)

    def in_order(self):
        a = self.klass.objects.create(name='a', group='y')
        self.klass.objects.create(name='b', group='y')
        self.klass.objects.create(name='c', group='y')
        self.assertValues(a.grouped_filter(), 'a,b,c')

    def forced_order(self):
        a = self.klass.objects.create(name='a', group='y')
        self.klass.objects.create(name='c', group='y')
        self.klass.objects.create(name='b', rank=2, group='y')
        self.assertValues(a.grouped_filter(), 'a,b,c')

    def same_order(self):
        a = self.klass.objects.create(name='a', group='y')
        a.rank = 1
        a.save()
        self.klass.objects.create(name='c', group='y')
        self.klass.objects.create(name='b', rank=2, group='y')
        self.assertValues(a.grouped_filter(), 'a,b,c')

    def negative(self):
        b = self.klass.objects.create(name='b', rank=-10, group='y')
        self.assertEqual(1, b.rank)

        a = self.klass.objects.create(name='a', rank=-10, group='y')
        self.assertEqual(1, a.rank)
        self.assertValues(a.grouped_filter(), 'a,b')

    def too_large(self):
        a = self.klass.objects.create(name='a', rank=10, group='y')
        self.assertEqual(1, a.rank)

        b = self.klass.objects.create(name='b', rank=10, group='y')
        self.assertEqual(2, b.rank)
        self.assertValues(a.grouped_filter(), 'a,b')

    def move(self):
        a = self.klass.objects.create(name='a', group='y')
        self.klass.objects.create(name='b', group='y')
        d = self.klass.objects.create(name='d', group='y')
        c = self.klass.objects.create(name='c', group='y')

        # test a simple move
        #import pudb; pudb.set_trace()
        c.rank -= 1
        c.save()
        self.assertValues(a.grouped_filter(), 'a,b,c,d')

        # test an out of bounds move
        d = refetch(d)
        d.rank += 5
        d.save()
        d = refetch(d)
        self.assertEqual(4, d.rank)
        self.assertValues(a.grouped_filter(), 'a,b,c,d')

        # test moving in the list
        a = refetch(a)
        a.rank += 2
        a.save()
        self.assertValues(a.grouped_filter(), 'b,c,a,d')

        a = refetch(a)
        a.rank = 0
        a.save()
        a = refetch(a)
        self.assertEqual(1, a.rank)
        self.assertValues(a.grouped_filter(), 'a,b,c,d')

    def repack(self):
        a = self.klass.objects.create(name='a', group='y')
        b = self.klass.objects.create(name='b', group='y')
        c = self.klass.objects.create(name='c', group='y')
        d = self.klass.objects.create(name='d', group='y')

        b.delete()
        a.repack()
        a = refetch(a)
        self.assertEqual(1, a.rank)
        c = refetch(c)
        self.assertEqual(2, c.rank)
        d = refetch(d)
        self.assertEqual(3, d.rank)
        self.assertValues(a.grouped_filter(), 'a,c,d')

    def admin(self):
        self.initiate()

        a = self.klass.objects.create(name='a', group='y')
        b = self.klass.objects.create(name='b', group='y')
        c = self.klass.objects.create(name='c', group='y')

        rank_admin = RankAdmin(self.klass, self.site)

        self.assertEqual('', self.field_value(rank_admin, a, 'move_up'))
        self.assertNotEqual('', self.field_value(rank_admin, b, 'move_up'))
        self.assertNotEqual('', self.field_value(rank_admin, c, 'move_up'))

        self.assertNotEqual('', self.field_value(rank_admin, a, 'move_down'))
        self.assertNotEqual('', self.field_value(rank_admin, b, 'move_down'))
        self.assertEqual('', self.field_value(rank_admin, c, 'move_down'))

        html = self.field_value(rank_admin, a, 'move_both')
        self.assertEqual( html.count('rankedmodel/move'), 1 )

        html = self.field_value(rank_admin, b, 'move_both')
        self.assertEqual( html.count('rankedmodel/move'), 2 )

        html = self.field_value(rank_admin, c, 'move_both')
        self.assertEqual( html.count('rankedmodel/move'), 1 )

        # use the view to move b up one
        headers = {
            'HTTP_REFERER':'/admin/',
        }
        self.visit_admin_link(rank_admin, b, 'move_up', response_code=302, 
            headers=headers)
        self.assertValues(a.grouped_filter(), 'b,a,c')

        # use the view to move a down one
        a = refetch(a)
        self.visit_admin_link(rank_admin, a, 'move_down', response_code=302,
            headers=headers)
        self.assertValues(a.grouped_filter(), 'b,c,a')

        # Use the up-link from the "move_both" column 
        #   -> url for c has two links, first match is up, regex group(1) 
        #   is the link portion of the regex
        c = refetch(c)
        html = self.field_value(rank_admin, c, 'move_both')
        pattern = re.compile('href="([^"]*)')
        url = list(pattern.finditer(html))[0].group(1)

        self.authed_get(url, response_code=302, headers=headers)
        self.assertValues(c.grouped_filter(), 'c,b,a')
        
        # Use the down-link from the "move_both" column
        #   -> url for b has two links, second match is down, regex group(1) 
        #   is the link portion of the regex
        b = refetch(b)
        html = self.field_value(rank_admin, b, 'move_both')
        pattern = re.compile('href="([^"]*)')
        url = list(pattern.finditer(html))[1].group(1)

        self.authed_get(url, response_code=302, headers=headers)
        self.assertValues(c.grouped_filter(), 'c,a,b')


class AloneTests(RankModelBase):
    def setUp(self):
        self.klass = Alone

    def test_in_order(self):
        self.in_order()

    def test_forced_order(self):
        self.forced_order()

    def test_same_order(self):
        self.same_order()

    def test_negative(self):
        self.negative()

    def test_too_large(self):
        self.too_large()

    def test_move(self):
        self.move()

    def test_repack(self):
        self.repack()

    def test_admin(self):
        self.admin()


class GroupedTests(RankModelBase):
    # Run the same tests as AloneTest, but have sub groups, at the end of each
    # test make sure that the "x" group (which isn't manipulated) is not
    # effected
    def setUp(self):
        self.klass = Grouped
        Grouped.objects.create(group='x', name='a')
        Grouped.objects.create(group='x', name='b')
        Grouped.objects.create(group='x', name='c')
        Grouped.objects.create(group='x', name='d')

    def test_in_order(self):
        self.in_order()
        self.assertValues(self.klass.objects.filter(group='x'), 'a,b,c,d')

    def test_forced_order(self):
        self.forced_order()
        self.assertValues(self.klass.objects.filter(group='x'), 'a,b,c,d')

    def test_same_order(self):
        self.same_order()
        self.assertValues(self.klass.objects.filter(group='x'), 'a,b,c,d')

    def test_negative(self):
        self.negative()
        self.assertValues(self.klass.objects.filter(group='x'), 'a,b,c,d')

    def test_too_large(self):
        self.too_large()
        self.assertValues(self.klass.objects.filter(group='x'), 'a,b,c,d')

    def test_move(self):
        self.move()
        self.assertValues(self.klass.objects.filter(group='x'), 'a,b,c,d')

    def test_repack(self):
        self.repack()
        self.assertValues(self.klass.objects.filter(group='x'), 'a,b,c,d')

    def test_admin(self):
        self.admin()
        self.assertValues(self.klass.objects.filter(group='x'), 'a,b,c,d')
