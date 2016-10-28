# create_test_data.py

from django.core.management.base import BaseCommand

from app.models import Nested, Inner, Outer

# =============================================================================

class Command(BaseCommand):
    def handle(self, *args, **options):
        n = Nested.objects.create(name='n1')
        i = Inner.objects.create(name='i1', nested=n)
        o = Outer.objects.create(name='o1.1', inner=i)
        o = Outer.objects.create(name='o1.2', inner=i)

        n = Nested.objects.create(name='n2')
        i = Inner.objects.create(name='i2', nested=n)
        o = Outer.objects.create(name='o2.1', inner=i)
