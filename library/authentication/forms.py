from django import forms
from .models import CustomUser, ROLE_CHOICES

class CustomUserForm(forms.ModelForm):
    # перевизначаємо віджет пароля, щоб символи приховувалися при введенні
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введіть пароль'}),
        label="Пароль"
    )

    class Meta:
        model = CustomUser
        fields = ["email", "password", "first_name", "last_name", "middle_name", "role"]
        
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@mail.com'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(choices=ROLE_CHOICES, attrs={'class': 'form-control'}),
        }


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email'}),
        label="Електронна пошта"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'password'}),
        label="Пароль"
    )