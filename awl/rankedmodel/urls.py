from django.conf.urls import url
from awl.rankedmodel import views

urlpatterns = [
    url(r'^move/(\d+)/(\d+)/(\d+)/$', views.move, name='awl-rankedmodel-move'),
]
