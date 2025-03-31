from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Task

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'gender', 'date_of_birth', 'is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('email', 'gender', 'date_of_birth')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )

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
    list_display = ['title', 'description', 'completed', 'created_at', 'get_users']
    search_fields = ('title', 'description')
    list_filter = ('completed', 'created_at')
    ordering = ('-created_at',)

    def get_users(self, obj):
        return ", ".join([user.username for user in obj.users.all()])
    get_users.short_description = 'Users'

    filter_horizontal = ('users',)




admin.site.register(CustomUser, CustomUserAdmin)
