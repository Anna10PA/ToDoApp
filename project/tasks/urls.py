from django.urls import path
from .views import tasks, add_new_task, all_tasks, delete, del_page, delete_all, delete_from_delete, completed, return_from_delete, edit, add_category, view_category, delete_category, edit_category, view_task


urlpatterns = [
    path('', tasks, name='tasks'),
    path('add_item/', add_new_task, name='add_new_task'),
    path('all/', all_tasks, name='all'),
    path('delete/<int:id>', delete, name='delete'),
    path('delete/', del_page, name='del_page'),
    path('delete_all/', delete_all, name='delete_all'),
    path('delete_from_delete/<int:id>', delete_from_delete, name='delete_from_delete'),
    path('completed/<int:id>', completed, name='completed'),
    path('return_from_delete/<int:id>', return_from_delete, name='return_from_delete'),
    path('edit/<int:id>', edit, name='edit'),
    path('add_category/', add_category, name='add_category'),
    path('view_category/', view_category, name='view_category'),
    path('delete_category/<str:ctg>', delete_category, name='delete_category'),
    path('edit_category/<str:ctg>', edit_category, name='edit_category'),
    path('view/<int:id>', view_task, name='views_tsks')
]
