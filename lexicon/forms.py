from django import forms
from .models import Word, City, Region
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class WordForm(forms.ModelForm):
    class Meta:
        model = Word
        fields = ['word', 'meaning', 'example', 'city']
        widgets = {
            'word': forms.TextInput(attrs={'class': 'form-control'}),
            'meaning': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'example': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'city': forms.Select(attrs={'class': 'form-control'}),
        }

class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['name', 'region', 'population', 'founded_year']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'region': forms.Select(attrs={'class': 'form-control'}),
            'population': forms.NumberInput(attrs={'class': 'form-control'}),
            'founded_year': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})