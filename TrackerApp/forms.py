from django.contrib.auth.forms import AuthenticationForm
from django import forms


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Your Email Here.",
        widget=forms.EmailInput(
            attrs={
                "class": "w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500",
                "placeholder": "Your email",
            }
        ),
    )
    password = forms.CharField(
        label="Your Password Here.",
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500",
                "placeholder": "Your email",
            }
        ),
    )
