from django.conf.urls import include, url
from django.contrib import admin

from awl.rankedmodel import urls as ranked_urls

urlpatterns = [
    url(r'admin/', include(admin.site.urls)),

    url(r'rankedmodel/', include(ranked_urls)),

    url(r'awl_test_views/test_view_for_messages/$', 
        'awl.tests.views.test_view_for_messages', ),
]
