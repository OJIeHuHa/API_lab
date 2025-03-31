from django.contrib.auth import get_user_model, login, logout, authenticate
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import status, generics, viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.views.generic import TemplateView,ListView
from django.utils import timezone
from django.contrib.sessions.models import Session
from .models import Task
from .serializers import UserSerializer, TaskSerializer

User = get_user_model()


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return

class OnlineUsersView(ListView):
    model = User
    template_name = 'online_users.html'
    context_object_name = 'online_users'

    def get_queryset(self):
        now = timezone.now()

        sessions = Session.objects.filter(expire_date__gte=now)

        online_users = []
        for session in sessions:
            data = session.get_decoded()
            user_id = data.get('_auth_user_id')
            if user_id:
                try:
                    user = User.objects.get(id=user_id)
                    online_users.append(user)
                except User.DoesNotExist:
                    continue

        return online_users


class RegisterView(TemplateView):
    template_name = "register.html"

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        gender = request.POST.get("gender")
        date_of_birth = request.POST.get("date_of_birth")

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                gender=gender,
                date_of_birth=date_of_birth
            )
            login(request, user)
            return redirect("/api/show/")
        except Exception as e:
            error = str(e)
            return render(request, "register.html", {"error": error})



class LoginView(TemplateView):
    template_name = "login.html"

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/api/show/")
        else:
            error = "Invalid username or password"
            return render(request, "login.html", {"error": error})



class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [CsrfExemptSessionAuthentication, BasicAuthentication]

    def post(self, request):
        logout(request)
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)



class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user



class AboutView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response(
            {
                "title": "About Us",
                "description": "Welcome to our To-Do List API!",
                "image_url": "https://via.placeholder.com/600x300"
            },
            status=status.HTTP_200_OK
        )

class TaskListView(ListView):
    model = Task
    template_name = "task_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.filter(users=self.request.user)



class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(users=self.request.user)

    def perform_create(self, serializer):
        task = serializer.save()
        task.users.add(self.request.user)

    def update(self, request, *args, **kwargs):
        task = self.get_object()

        if request.user not in task.users.all():
            return Response({"error": "You do not have permission to edit this task."}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        task = self.get_object()

        if request.user not in task.users.all():
            return Response({"error": "You do not have permission to delete this task."}, status=status.HTTP_403_FORBIDDEN)

        task.delete()
        return Response({"message": "Task deleted successfully."}, status=status.HTTP_200_OK)


class TaskDetailPageView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        if request.user not in task.users.all():
            return render(request, "403.html", status=403)

        all_users = User.objects.all()
        return render(request, "task_detail.html", {"task": task, "all_users": all_users})


class AddUserToTaskView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        user_id = request.data.get("user_id")
        user = get_object_or_404(User, id=user_id)
        task.users.add(user)
        task.save()
        return redirect("task_detail_page", task_id=task.id)
