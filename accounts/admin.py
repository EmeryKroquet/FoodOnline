from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import UserProfile
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    readonly_fields = ('date_joined', 'last_login')  # Ces champs ne doivent pas être éditables

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_active', 'is_superadmin', 'role')}),
        ('Important dates', {'fields': ('last_login',)}),  # Excluez 'date_joined' ici
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'city', 'country', 'created_at')
    search_fields = ('user__email', 'city', 'country')
    list_filter = ('country', 'state', 'city')
    readonly_fields = ('created_at', 'modified_at')

    fieldsets = (
        (None, {
            'fields': ('user', 'profile_picture', 'cover_photo', 'address', 'city', 'state', 'country', 'pin_code', 'latitude', 'longitude', 'location')
        }),
        ('Important dates', {
            'fields': ('created_at', 'modified_at')
        }),
    )

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username


# Register the UserAdmin with the User model
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)