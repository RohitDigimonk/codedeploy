from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('add-iteration', views.add_iteration, name='add_iteration'),
    path('add-iteration/', views.add_iteration, name='add_iteration'),

    path('get_backlogs', views.get_backlogs, name='get_backlogs'),

    path('get_user_story', views.get_user_story, name='get_user_story'),

    path('edit-iteration/<int:id>', views.edit_iteration, name='edit_iteration'),
    path('edit-iteration/<int:id>/', views.edit_iteration, name='edit_iteration'),

    path('remove-iteration/<int:id>/', views.remove_iteration, name='remove_iteration'),
]