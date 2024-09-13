from django import forms
from .models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'role']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        email = cleaned_data.get('email')
        username = cleaned_data.get('username')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("An account with this username already exists.")

        return cleaned_data

