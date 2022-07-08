from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class ConvertForm(forms.Form):
    long_url = forms.CharField(label='URL для сокращения')

    def clean_long_url(self):
        long_url = self.cleaned_data['long_url']
        if not long_url.startswith('https://'):
            raise ValidationError('URL должен начинаться с `https://`')
        return long_url


class RegistrationUserForm(UserCreationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='repeat password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        data = self.cleaned_data['email']
        if '@gmail.com' not in data:
            raise ValidationError('email should contain `@gmail.com`')
        return data
