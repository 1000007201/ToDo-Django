from django.urls import path
from .views import TaskView, TestView, TaskCountView

urlpatterns = [
    path('api/tasks', TaskView.as_view()),
    path('api/tasks/<int:id>', TaskView.as_view()),
    path('api/task/test', TestView.as_view()),
    path('api/tasks/count', TaskCountView.as_view())
]
