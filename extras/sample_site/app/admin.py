from django.contrib import admin

from app.models import Nested, Inner, Outer
from awl.admintools import make_admin_obj_mixin

# Register your models here.

@admin.register(Nested)
class NestedAdmin(admin.ModelAdmin):
    list_display = ('name', )


base = make_admin_obj_mixin('InnerMeta')
base.add_obj_link('show_nested', 'nested')

# ??? not sure what the filter was doing, attribute DNE anymore
#base.add_obj_link('show_parents', 'outer', 'All Outer Parents', 
#    attr_filter='outer__id')
base.add_obj_link('show_parents', 'outer', 'All Outer Parents')

@admin.register(Inner)
class InnerAdmin(admin.ModelAdmin, base):
    list_display = ('name', 'show_nested', 'show_parents')


base = make_admin_obj_mixin('OuterMeta')
base.add_obj_link('show_nested', 'inner__nested', 'foo', 'nested={{obj.id}}')
base.add_obj_link('show_inner', 'inner')

@admin.register(Outer)
class OuterAdmin(admin.ModelAdmin, base):
    list_display = ('name', 'show_inner', 'show_nested')
