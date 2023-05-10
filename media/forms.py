from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from .models import Movie, Media
from django.db.models import Q
from django.core.validators import FileExtensionValidator
from django_otp.forms import OTPAuthenticationFormMixin
import os
from django.conf import settings
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


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
                print('existe')
            except User.DoesNotExist:
                print('nãoexiste')
                raise forms.ValidationError('Invalid username or email')
        return username

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError('User account is disabled.')


class CreateMovieForm(forms.ModelForm):
    duration = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input_text'})
    )

    CLASSIFICATION_CHOICES = (
        ('L', 'Livre'),
        ('10', 'Não recomendado para menores de 10 anos'),
        ('12', 'Não recomendado para menores de 12 anos'),
        ('14', 'Não recomendado para menores de 14 anos'),
        ('16', 'Não recomendado para menores de 16 anos'),
        ('18', 'Não recomendado para menores de 18 anos'),
    )

    classification = forms.ChoiceField(
        choices=CLASSIFICATION_CHOICES,
        widget=forms.Select(attrs={'class': 'input_text'})
    )


    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input_text'})
    )

    release_year = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'input_text'})
    )

    poster = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'input_button', 'id': 'input_poster', 'hidden': 'hidden'})
    )

    banner = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'input_button', 'id': 'input_banner', 'hidden': 'hidden'})
    )

    title_img = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'input_button', 'id': 'input_title', 'hidden': 'hidden'})
    )

    media_file = forms.FileField(
        validators=[
            FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv', 'h264'])
        ],
        widget=forms.ClearableFileInput(attrs={'class': 'input_button', 'id': 'input_media', 'hidden': 'hidden'})
    )

    trailer = forms.FileField(
        validators=[
            FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv', 'h264'])
        ],
        widget=forms.ClearableFileInput(attrs={'class': 'input_trailer', 'hidden': 'hidden'})
    )

    class Meta:
        model = Movie
        fields = ('title', 'description', 'short_description', 'release_year', 'duration', 'classification',  'poster', 'banner', 'title_img', 'media_file', 'trailer')

    def save(self, commit=True):
        media = Media(
            title=self.cleaned_data['title'],
            release_year=self.cleaned_data['release_year'],
            poster=self.cleaned_data['poster'],
            banner=self.cleaned_data['banner'],
            title_img=self.cleaned_data['title_img'],
            media_file=self.cleaned_data['media'],
            trailer=self.cleaned_data['trailer'],
        )
        media.save()

        movie = super(CreateMovieForm, self).save(commit=False)
        movie.media = media

        if commit:
            movie.save()

        if 'media_file' in self.files:
            media_file = self.files['media_file']
            movie.media_path = os.path.join(settings.MEDIA_ROOT, 'static/media/video', media_file.name)
            with open(movie.media_path, 'wb') as media_dest:
                for chunk in media_file.chunks():
                    media_dest.write(chunk)

        if 'trailer_file' in self.files:
            trailer_file = self.files['trailer_file']
            movie.trailer_path = os.path.join(settings.MEDIA_ROOT, 'static/media/trailer', trailer_file.name)
            with open(movie.trailer_path, 'wb') as trailer_dest:
                for chunk in trailer_file.chunks():
                    trailer_dest.write(chunk)

        if commit:
            movie.save()

        return movie


class CreateUserForm(UserCreationForm):
    photo = forms.ImageField(required=False)
    telephone = forms.IntegerField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'telephone', 'password1', 'password2', 'photo']


class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        label='',
        widget=forms.TextInput(attrs={"autofocus": True, 'class': 'input_login', 'placeholder': 'Digite seu username'}),
    )
    password = forms.CharField(
        label='',
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password", 'placeholder': 'Digite sua senha'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'custom-class-1', 'placeholder': 'Digite o nome de usuário'})
        self.fields['password'].widget.attrs.update({'class': 'custom-class-2', 'placeholder': 'Digite a senha'})
