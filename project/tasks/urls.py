from django.urls import path
from .views import tasks, add_new_task, all_tasks, delete, del_page, delete_all, delete_from_delete, completed, return_from_delete, edit


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
    path('edit/<int:id>', edit, name='edit')
]
