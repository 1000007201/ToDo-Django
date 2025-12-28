from django.urls import path
from .views import TaskView, TaskCountView, list_tasks_page, add_task_page

urlpatterns = [
    path('', list_tasks_page),
    path('add-task/', add_task_page),
    path('api/tasks/', TaskView.as_view()),
    path('api/tasks/<int:id>', TaskView.as_view()),
    path('api/tasks/count/', TaskCountView.as_view())
]
