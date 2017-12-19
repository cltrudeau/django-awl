import django
from django.contrib import admin

from awl.rankedmodel import urls as ranked_urls
from awl.tests import views

# django 1.11 and 2.0 have different URL path mechanisms 
if django.VERSION[0] >= 2:
    from django.urls import include, path

    urlpatterns = [
        path('admin/', admin.site.urls),

        path('rankedmodel/', include(ranked_urls)),

        path('awl_test_views/test_view_for_messages/', 
            views.test_view_for_messages, ),
    ]
else: # pragma: no cover
    from django.conf.urls import include, url

    urlpatterns = [
        url(r'^admin/', admin.site.urls),

        url(r'^rankedmodel/', include(ranked_urls)),

        url(r'^awl_test_views/test_view_for_messages/$', 
            views.test_view_for_messages, ),
    ]
