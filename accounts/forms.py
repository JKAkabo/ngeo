from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'autofocus': '',
            'placeholder': 'Username',
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
        }
    ))


class StaffRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'password',
        ]


class ConfirmStaffRegistrationForm(forms.Form):
    username = forms.MultipleChoiceField(choices=(('hello', 'world'), ('jarvis', 'ai')))
