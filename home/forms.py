from django import forms
from django.utils.safestring import mark_safe
from . import views

class RechercheDeezer(forms.Form):
    CHOICES=[('MP3','MP3'), ('MP4','MP4')]
    recherche = forms.CharField()
    debut = forms.CharField(required=False)
    fin = forms.CharField(required=False)