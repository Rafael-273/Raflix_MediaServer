from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Movie
from django.db.models import Q
from django.core.validators import FileExtensionValidator


# class LoginForm(AuthenticationForm):
#     username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={'autofocus': True}))
#     password = forms.CharField(label=("Password"), widget=forms.PasswordInput)
#     remember_me = forms.BooleanField(required=False, initial=True, widget=forms.CheckboxInput())

#     error_messages = {
#         'invalid_login': (
#             "Please enter a correct %(username)s and password. Note that both "
#             "fields may be case-sensitive."
#         ),
#         'inactive': ("This account is inactive."),
#     }   

#     def clean_username(self):
#         username = self.cleaned_data.get('username')
#         print('\n________________',username)
#         if username:
#             try:
#                 User.objects.get(Q(username=username) | Q(email=username))
#                 print('existe')
#                 print(User.objects.get(Q(username=username) | Q(email=username)))
#             except User.DoesNotExist:
#                 print('nãoexiste')
#                 raise forms.ValidationError('Invalid username or email')
#         return username

#     def confirm_login_allowed(self, user):
#         if not user.is_active:
#             print('não ta ativo')
#             raise forms.ValidationError('User account is disabled.')


class CreateMovieForm(forms.ModelForm):
    duration = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input_text'})
    )

    classification = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input_text'})
    )

    media = forms.FileField(
        validators=[
            FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv','h264'])
        ], 
        widget=forms.TextInput(attrs={'type': 'file', 'class': 'input_button'})
    )
    trailer = forms.FileField(
        validators=[
            FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv','h264'])
        ], 
        widget=forms.TextInput(attrs={'type': 'file', 'class': 'input_button'})
    )
    class Meta:
        model = Movie
        fields = ('description', 'short_description', 'duration', 'classification', 'media', 'trailer')
