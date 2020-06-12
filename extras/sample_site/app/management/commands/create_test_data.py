# create_test_data.py

from django.core.management.base import BaseCommand

from app.models import Writer, Show, Episode

# =============================================================================

class Command(BaseCommand):
    def handle(self, *args, **options):
        writer = Writer.objects.create(name='Douglas Adams')
        show = Show.objects.create(title='Dirk Gently', writer=writer)
        episode = Episode.objects.create(name='Space Rabbit', show=show)
        episode = Episode.objects.create(name='Fans of Wet Circles', show=show)

        writer = Writer.objects.create(name='G.R.R Martin')
        show = Show.objects.create(title='Game of Thrones', writer=writer)
        episode = Episode.objects.create(name='Dragonstone', show=show)
        episode = Episode.objects.create(name='Stormborn', show=show)

        Show.objects.create(title='Episodeless', writer=writer)

        show = Show.objects.create(title='Simpsons')
        episode = Episode.objects.create(name='TreeHouse of Horror III', 
            show=show)

        Episode.objects.create(name='Without Show')
