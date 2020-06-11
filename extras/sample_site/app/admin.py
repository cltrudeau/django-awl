from django.contrib import admin

from app.models import Writer, Show, Episode
from awl.tests.models import Author, Book, Chapter
from awl.admintools import make_admin_obj_mixin, fancy_modeladmin

# remove the awl.test admin files, they confuse things
admin.site.unregister(Author)
admin.site.unregister(Book)
admin.site.unregister(Chapter)


@admin.register(Writer)
class WriterAdmin(admin.ModelAdmin):
    list_display = ('name', )


base = fancy_modeladmin('title')
base.add_fk_link('episode_set', Episode)

@admin.register(Show)
class ShowAdmin(base):
    pass


base = fancy_modeladmin('name')
base.add_link('show__writer', 'This is the Writer Column Title', 
    'writer={{obj.id}}')
base.add_link('show')
base.add_object('show__writer', 'Read-Only Writer Column', 
    '{{obj.name}} (id={{obj.id}})')

@admin.register(Episode)
class EpisodeAdmin(base):
    pass
