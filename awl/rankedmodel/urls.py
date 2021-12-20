from django.urls import path
from awl.rankedmodel import views

urlpatterns = [
    path('move/<int:content_type_id>/<int:obj_id>/<int:rank>/', views.move, 
        name='awl-rankedmodel-move'),
]
