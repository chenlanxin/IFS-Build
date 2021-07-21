from django.urls import path

from . import views

urlpatterns = [
    path('get_task/<int:top>', views.get_tasks, name='get tasks')
]
