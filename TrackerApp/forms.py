from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import CustomUser, Task


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


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "class": "w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500",
                "placeholder": "Your email",
            }
        ),
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500",
                "placeholder": "Enter password",
            }
        ),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500",
                "placeholder": "Confirm password",
            }
        ),
    )

    class Meta:
        model = CustomUser
        fields = ("email", "password1", "password2")


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "task_name",
            "start_date",
            "est_end_date",
            "category",
            "numeric_target",
            "numeric_current",
            "status",
            "priority",
            "notes",
        ]
        widgets = {
            "task_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Task Name"}
            ),
            "start_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "est_end_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "numeric_target": forms.NumberInput(attrs={"class": "form-control"}),
            "numeric_current": forms.NumberInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "priority": forms.Select(attrs={"class": "form-select"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
