# forms.py

from django import forms
from .models import Movie, Show, ToWatchShow, ToWatchMovie

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'duration']

class ShowForm(forms.ModelForm):
    class Meta:
        model = Show
        fields = ['title', 'duration']

class ToWatchShowForm(forms.ModelForm):
    class Meta:
        model = ToWatchShow
        fields = ['title', 'duration', 'notes']

class ToWatchMovieForm(forms.ModelForm):
    class Meta:
        model = ToWatchMovie
        fields = ['title', 'duration', 'notes']