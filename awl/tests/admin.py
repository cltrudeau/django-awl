from django.contrib import admin

from awl.tests.models import Link, Inner, Outer, Nested
from awl.admintools import make_admin_obj_mixin

# ============================================================================
# Waelsteng Admin Models
# ============================================================================

class LinkAdmin(admin.ModelAdmin):
    list_display = ('url', 'text', 'visit_me')

    def visit_me(self, obj):
        return '<a href="%s">%s</a>' % (obj.url, obj.text)

# ============================================================================
# Admintools Admin Models
# ============================================================================

@admin.register(Nested)
class NestedAdmin(admin.ModelAdmin):
    list_display = ('name', )


base = make_admin_obj_mixin('InnerMixin')
base.add_obj_link('show_nested', 'nested')

@admin.register(Inner)
class InnerAdmin(admin.ModelAdmin, base):
    list_display = ('name', 'show_nested')


base = make_admin_obj_mixin('OuterMixin')
base.add_obj_link('show_nested', 'inner__nested')
base.add_obj_link('show_inner', 'inner', 'My Inner', 'Inner.id={{obj.id}}')

@admin.register(Outer)
class OuterAdmin(admin.ModelAdmin, base):
    list_display = ('name', 'show_inner', 'show_nested')
