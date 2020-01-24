from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('/<str:set_statue>/<str:set_statue_2>', views.index, name='index'),
    # path('/<str:set_statue>/<str:set_statue_2>/<str:csv_id>', views.index, name='index'),

    path('add-new', views.add_user_story_view, name='add_user_story_view'),
    path('get_file_data', views.get_file_data, name='get_file_data'),

    path('add-new/', views.add_user_story_view, name='add_user_story_view'),

    path('get-data', views.get_data, name='get_data'),
    path('get-data/', views.get_data, name='get_data'),

    path('add-csv-files/', views.add_csv_files, name='add_csv_files'),
    path('add-csv-files', views.add_csv_files, name='add_csv_files'),

    path('edit-story/<int:id>', views.edit_user_story_view, name='edit_user_story_view'),
    path('edit-story/<int:id>/', views.edit_user_story_view, name='edit_user_story_view'),

    path('remove-user-story/<int:id>', views.delete_user_story_view, name='delete_user_story_view'),
    path('remove-user-story/<int:id>/', views.delete_user_story_view, name='delete_user_story_view'),

    path('create-copys/<str:ids>', views.select_user_story_view, name='select_user_story_view'),
    path('create-copys/<str:ids>/', views.select_user_story_view, name='select_user_story_view'),

    path('update-table-structure/<str:columnnames>/', views.update_table_structure, name='update_table_structure'),
    path('update-table-structure/<str:columnnames>/', views.update_table_structure, name='update_table_structure'),
]