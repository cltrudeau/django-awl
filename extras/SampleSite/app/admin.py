from django.contrib import admin

from app.models import Writer, Show, Episode, Station
from awl.tests.models import Author, Book, Chapter
from awl.admintools import fancy_modeladmin

# remove the awl.test admin files, they confuse things
admin.site.unregister(Author)
admin.site.unregister(Book)
admin.site.unregister(Chapter)


@admin.register(Writer)
class WriterAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ('name', )


# ShowAdmin
base = fancy_modeladmin('title')
base.add_fk_link('episode_set', Episode, 'episode')
base.add_fk_link('episode_set', Episode, 'episode', title='Episode with Empty', 
    empty='<i>no episodes</i>')
base.add_m2m_link('stations', 'Station')

@admin.register(Show)
class ShowAdmin(base):
    pass


# EpisodeAdmin
base = fancy_modeladmin('name')
base.add_link('show__writer', 'This is the Writer Column Title', 
    'writer={{obj.id}}')
base.add_link('show')
base.add_object('show__writer', 'Read-Only Writer Column', 
    '{{obj.name}} (id={{obj.id}})')
base.add_object('show__writer', 'Read-Only Writer with Empty', 
    '{{obj.name}} (id={{obj.id}})', '<i>no writer</i>')
base.add_display('name', 'Name Column With Empty', '<i>no name</i>')

base.add_link('show', title='Show with Empty', empty='<i>no show</i>')
base.add_templated_field('name', 'Name={{field}} Row.id={{row.id}}', 
    'Templated Column')

@admin.register(Episode)
class EpisodeAdmin(base):
    pass
