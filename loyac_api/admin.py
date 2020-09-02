from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Applicant, Program, AgeGroup


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password',
                           'first_name', 'last_name', 'birth_date')}),
        ('Permissions', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'user_permissions',
        )}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password')
            }
        ),
    )

    list_display = ('email', 'first_name', 'last_name',
                     'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active',)
    filter_horizontal = ('groups', 'user_permissions',)
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(User, UserAdmin)
admin.site.register(Applicant)
admin.site.register(Program)
admin.site.register(AgeGroup)