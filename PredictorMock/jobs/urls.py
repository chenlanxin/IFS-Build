from django.urls import path

from . import views

urlpatterns = [
    path('get_ready_tasks', views.get_tasks, name='get tasks')
]
