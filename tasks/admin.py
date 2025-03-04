from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Task


class CustomUserAdmin(UserAdmin):
    # Fields to be displayed in the admin panel
    list_display = ('username', 'email', 'gender', 'date_of_birth', 'is_staff', 'is_active')

    # Fields to be used in the user edit form
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('email', 'gender', 'date_of_birth')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )

    # Fields for the user creation form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'gender', 'date_of_birth'),
        }),
    )

    search_fields = ('email', 'username')
    ordering = ('email',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'completed', 'user', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('completed', 'created_at')
    ordering = ('-created_at',)


# Register the model
admin.site.register(CustomUser, CustomUserAdmin)
