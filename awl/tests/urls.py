from django.contrib import admin

from awl.rankedmodel import urls as ranked_urls
from awl.tests import views

from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),

    path('rankedmodel/', include(ranked_urls)),

    path('awl_test_views/test_view_for_messages/', 
        views.test_view_for_messages, ),
]
