from django.conf.urls import patterns, url

urlpatterns = patterns('awl.rankedmodel.views',
    url(r'move/(\d+)/(\d+)/(\d+)/$', 'move', name='awl-rankedmodel-move'),
)
