from django.urls import path
from .views import register, log_in, log_out, profile, about, create_task, list_tasks, update_task, delete_task
urlpatterns = [
    path('register/', register),
    path('login/', log_in),
    path('logout/', log_out),
    path('profile/', profile),
    path('about/', about),

    path('create/', create_task),
    path('show/', list_tasks),
    path("update/<int:task_id>/", update_task, name="update_task"),
    path("delete/<int:task_id>/", delete_task, name="delete_task"),
]