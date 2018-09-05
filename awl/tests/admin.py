from django.contrib import admin

from awl.admintools import make_admin_obj_mixin, fancy_modeladmin
from awl.tests.models import (Link, Author, Book, Chapter, Driver,
    VehicleMake, VehicleModel)
from awl.rankedmodel.admintools import admin_link_move_up, admin_link_move_down

# ============================================================================
# Waelsteng Admin Models
# ============================================================================

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('url', 'text', 'visit_me')

    def visit_me(self, obj):
        return '<a href="%s">%s</a>' % (obj.url, obj.text)

# ============================================================================
# Admintools Admin Models
# ============================================================================

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', )


base = make_admin_obj_mixin('BookMixin')
base.add_obj_link('show_author', 'author')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin, base):
    list_display = ('name', 'show_author')


base = make_admin_obj_mixin('ChapterMixin')
base.add_obj_link('show_author', 'book__author')
base.add_obj_link('show_book', 'book', 'My Book', 
    '{{obj.classname}}.id={{obj.id}}')
base.add_obj_ref('readonly_author', 'book__author')
base.add_obj_ref('readonly_book', 'book', 'Readonly Book', 
    'RO {{obj.classname}}.id={{obj.id}}')

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin, base):
    list_display = ('name', 'show_author', 'show_book', 'readonly_author',
        'readonly_book')

# ----------------------------------------------------------------------------

base = fancy_modeladmin('id')
base.add_displays('name')
base.add_link('vehiclemodel__vehiclemake')
base.add_link('vehiclemodel', 'My Vehicle Model', 
    '{{obj.fullname}} id={{obj.id}}')
base.add_object('vehiclemodel__vehiclemake')
base.add_object('vehiclemodel', 'RO Vehicle Model', 
    'RO {{obj.fullname}} id={{obj.id}}')
base.add_formatted_field('rating', '%0.1f')

@admin.register(Driver)
class DriverAdmin(base):
    pass


@admin.register(VehicleMake)
class VehicleMakeAdmin(admin.ModelAdmin):
    pass


base = fancy_modeladmin('id')
base.add_display('name')
base.add_display('year', 'YEAR TITLE')

@admin.register(VehicleModel)
class VehicleModelAdmin(base):
    pass

# ============================================================================
# RankedModel Admin Models
# ============================================================================

class RankAdmin(admin.ModelAdmin):
    list_display = ('name', 'move_up', 'move_down')

    def move_up(self, obj):
        return admin_link_move_up(obj)
    move_up.allow_tags = True
    move_up.short_description = 'Move Up Rank'

    def move_down(self, obj):
        return admin_link_move_down(obj)
    move_down.allow_tags = True
    move_down.short_description = 'Move Up Rank'
