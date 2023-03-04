from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User
from django.db.models import Q

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(label=("Password"), widget=forms.PasswordInput)
    remember_me = forms.BooleanField(required=False, initial=True, widget=forms.CheckboxInput())

    error_messages = {
        'invalid_login': (
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': ("This account is inactive."),
    }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            try:
                User.objects.get(Q(username=username) | Q(email=username))
            except User.DoesNotExist:
                raise forms.ValidationError('Invalid username or email')
        return username

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError('User account is disabled.')
