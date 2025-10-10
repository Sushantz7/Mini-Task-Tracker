from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Category, AuditLog, Task


class CustomUserAdmin(UserAdmin):
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Category)
admin.site.register(Task)
admin.site.register(AuditLog)
