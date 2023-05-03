from django import forms
from .models import Movie
from django.db.models import Q
from django.core.validators import FileExtensionValidator


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