from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from .models import Movie, Media, User, genre_choices, Genre
from django.db.models import Q
from django.core.validators import FileExtensionValidator
from django_otp.forms import OTPAuthenticationFormMixin
import os
from django.conf import settings
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
import re
from django.contrib.auth.forms import PasswordChangeForm


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

    category = forms.ChoiceField(
        choices=genre_choices,
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
        fields = ('title', 'description', 'short_description', 'release_year', 'duration', 'classification', 'category', 'poster', 'banner', 'title_img', 'media_file', 'trailer')

    def save(self, commit=True):
        media = Media(
            title=self.cleaned_data['title'],
            release_year=self.cleaned_data['release_year'],
            poster=self.cleaned_data['poster'],
            banner=self.cleaned_data['banner'],
            title_img=self.cleaned_data['title_img'],
            media_file=self.cleaned_data['media_file'],
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


class EditMovieForm(forms.ModelForm):
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

    category = forms.ChoiceField(
        choices=genre_choices,
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].initial = self.instance.media.title
        self.fields['release_year'].initial = self.instance.media.release_year
        self.fields['poster'].initial = self.instance.media.poster
        self.fields['banner'].initial = self.instance.media.banner
        self.fields['title_img'].initial = self.instance.media.title_img
        self.fields['media_file'].initial = self.instance.media.media_file
        self.fields['trailer'].initial = self.instance.media.trailer
        self.fields['category'].choices = genre_choices
        category_value = self.instance.media.getCategory()
        self.fields['category'].initial = category_value

    class Meta:
        model = Movie
        fields = ('title', 'description', 'short_description', 'release_year', 'duration', 'classification', 'category', 'poster', 'banner', 'title_img', 'media_file', 'trailer')

    def save(self, commit=True):
        movie = super(EditMovieForm, self).save(commit=False)

        media = movie.media
        media.title = self.cleaned_data['title']
        media.release_year = self.cleaned_data['release_year']
        media.poster = self.cleaned_data['poster']
        media.banner = self.cleaned_data['banner']
        media.title_img = self.cleaned_data['title_img']
        media.media_file = self.cleaned_data['media_file']
        media.trailer = self.cleaned_data['trailer']
        media.save()

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

        selected_genres = self.cleaned_data['category']
        movie.movie_has_genre.all().delete()

        for genre_initial in selected_genres:
            try:
                genre = Genre.objects.get(category__startswith=genre_initial)
                movie.movie_has_genre.create(genre=genre)
            except Genre.DoesNotExist:
                pass

        return movie


class TelephoneInput(forms.widgets.TextInput):
    def __init__(self, attrs=None):
        super().__init__(attrs)

        # Definição da expressão regular para o formato de telefone
        self.regex = re.compile(r'^\(?([0-9]{2})\)?[-. ]?([0-9]{4,5})[-. ]?([0-9]{4})$')

    def format_value(self, value):
        if value is None:
            return ''  # retorna uma string vazia se o valor for nulo
        match = self.regex.search(value)
        if match:
            return '({}){}-{}'.format(match.group(1), match.group(2), match.group(3))
        return value

    def get_validator(self):
        # Retorna um validador para o formato de telefone
        return RegexValidator(self.regex, _('Entre com um telefone válido.'))


class CreateUserForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input_text'})
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input_text'})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input_text'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'input_text'})
    )
    telephone = forms.CharField(
        label=_('Telefone'),
        max_length=14,
        required=True,
        validators=[TelephoneInput().get_validator()],
        widget=TelephoneInput(attrs={'class': 'input_text'})
    )
    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={'class': 'input_text'})
    )
    password2 = forms.CharField(
        label="Confirmação de senha",
        widget=forms.PasswordInput(attrs={'class': 'input_text'})
    )
    photo = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'input_text-file', 'hidden': 'hidden'})
    )

    is_superuser = forms.BooleanField(
        required=False, widget=forms.CheckboxInput()
    )

    def save(self, commit=True):
        username = self.cleaned_data['username']
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        email = self.cleaned_data['email']
        telephone = self.cleaned_data['telephone']
        password = self.cleaned_data['password1']
        photo = self.cleaned_data['photo']

        user = User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            telephone=telephone,
            password=password,
            photo=photo
        )

        return user

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'telephone', 'password1', 'password2', 'photo', 'is_superuser']


class EditUserForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input_text'})
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input_text'})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input_text'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'input_text'})
    )
    telephone = forms.CharField(
        label=_('Telefone'),
        max_length=14,
        required=True,
        validators=[TelephoneInput().get_validator()],
        widget=TelephoneInput(attrs={'class': 'input_text'})
    )
    old_password = forms.CharField(
        label="Senha Atual",
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'input_text'})
    )
    new_password1 = forms.CharField(
        label="Nova Senha",
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'input_text'})
    )
    new_password2 = forms.CharField(
        label="Confirme a Nova Senha",
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'input_text'})
    )
    photo = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'input_text-file', 'hidden': 'hidden'})
    )

    is_superuser = forms.BooleanField(
        required=False, widget=forms.CheckboxInput()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].initial = self.instance.username
        self.fields['first_name'].initial = self.instance.first_name
        self.fields['last_name'].initial = self.instance.last_name
        self.fields['email'].initial = self.instance.email
        self.fields['telephone'].initial = self.instance.telephone
        self.fields['photo'].choices = self.instance.photo
        self.fields['is_superuser'].initial = self.instance.is_superuser

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'telephone', 'photo', 'is_superuser']

    def save(self, commit=True):
        user = super().save(commit=False)

        username = self.cleaned_data['username']
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        email = self.cleaned_data['email']
        telephone = self.cleaned_data['telephone']
        photo = self.cleaned_data['photo']

        if self.cleaned_data.get('new_password1') and self.cleaned_data.get('new_password2'):
            old_password = self.cleaned_data.get('old_password')
            new_password1 = self.cleaned_data['new_password1']
            new_password2 = self.cleaned_data['new_password2']

            if not user.check_password(old_password):
                self.add_error('old_password', 'A senha atual está incorreta.')

            if new_password1 != new_password2:
                self.add_error('new_password2', 'As novas senhas não correspondem.')

            if not self.errors:
                if new_password1:
                    user.set_password(new_password1)

        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.telephone = telephone
        user.photo = photo

        if commit:
            user.save()

        return user


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
