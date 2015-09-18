from django.contrib import admin
from django.db import models

# ============================================================================
# Models used by tests

class Link(models.Model):
    url = models.CharField(max_length=80)
    text = models.CharField(max_length=80)

# ============================================================================
# Admin Models for tests

class LinkAdmin(admin.ModelAdmin):
    list_display = ('url', 'text', 'visit_me')

    def visit_me(self, obj):
        return '<a href="%s">%s</a>' % (obj.url, obj.text)
