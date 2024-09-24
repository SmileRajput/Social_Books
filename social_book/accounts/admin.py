from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UploadedFiles
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ['email', 'name', 'is_staff', 'is_active', 'public_visibility'] # noqa
    list_filter = ['is_staff', 'is_active', 'public_visibility']
    fieldsets = (
        (None, {'fields': ('email', 'name', 'password', 'address', 'birth_year', 'public_visibility')}), # noqa
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}), # noqa
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'address', 'birth_year', 'public_visibility', 'is_active', 'is_staff')} # noqa
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(UploadedFiles)
class UploadedFilesAdmin(admin.ModelAdmin):
    list_display = ('title', 'file', 'visibility', 'cost', 'year_published', 'uploaded_at') # noqa