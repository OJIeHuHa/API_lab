from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView, LoginView, LogoutView, ProfileView, AboutView,
    TaskViewSet, TaskDetailPageView, AddUserToTaskView, TaskListView,
    OnlineUsersView,
)

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('about/', AboutView.as_view(), name='about'),
    path('show/', TaskListView.as_view(), name='task_list'),
    path('task/<int:task_id>/', TaskDetailPageView.as_view(), name='task_detail_page'),
    path('task/<int:task_id>/add_user/', AddUserToTaskView.as_view(), name='add_user_to_task'),
    path('api/', include(router.urls)),
    path('online_users/', OnlineUsersView.as_view(), name='online_users'),
]
