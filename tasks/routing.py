from django.urls import path
from .consumers import TaskChatConsumer

websocket_urlpatterns = [
    path("ws/task/<int:task_id>/chat/", TaskChatConsumer.as_asgi()),
]