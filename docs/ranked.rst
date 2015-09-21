RankedModel
===========

.. automodule:: awl.rankedmodel.models
    :members:

RankedModel Admin
=================

Two admin helper functions are provided so you can do rank re-ording in
the django admin.  To use the helper functions you will need to have
``awl.rankedmodel`` in your ``INSTALLED_APPS`` and include the urls.

.. code-block:: python

    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'awl.rankedmodel',
    )

.. code-block:: python

    urlpatterns = [
        url(r'^admin/', include(admin.site.urls)),
        url(r'^rankedmodel/', include('rankedmodel.urls')),
    ]


The provided functions act return links to a django admin view that can move
the associated objects.  To use them, add them as columns in the admin model
of your inheriting class.

.. code-block:: python

    from awl.rankedmodel.admin import admin_link_move_up, admin_link_move_down

    @admin.register(Favourites)
    class FavouritesAdmin(admin.ModelAdmin):
        list_display = ('name', 'rank', 'move_up', 'move_down')

        def move_up(self, obj):
            return admin_link_move_up(obj)
        move_up.allow_tags = True
        move_up.short_description = 'Move Up Rank'

        def move_down(self, obj):
            return admin_link_move_down(obj)
        move_down.allow_tags = True
        move_down.short_description = 'Move Up Rank'


.. automodule:: awl.rankedmodel.admintools
    :members:
