from django.contrib import admin

from app.models import Writer, Show, Episode
from awl.tests.models import Author, Book, Chapter
from awl.admintools import make_admin_obj_mixin

# remove the awl.test admin files, they confuse things
admin.site.unregister(Author)
admin.site.unregister(Book)
admin.site.unregister(Chapter)


@admin.register(Writer)
class WriterAdmin(admin.ModelAdmin):
    list_display = ('name', )


base = make_admin_obj_mixin('ShowMixin')
base.add_obj_link('show_writer', 'writer')

@admin.register(Show)
class ShowAdmin(admin.ModelAdmin, base):
    list_display = ('title', 'show_writer')


base = make_admin_obj_mixin('EpisodeMixin')
base.add_obj_link('show_writer', 'show__writer', 
    'This is the Writer Column Title', 'writer={{obj.id}}')
base.add_obj_link('show_show', 'show')

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin, base):
    list_display = ('name', 'show_writer', 'show_show')
