from django import forms
from .models import Author

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ["name", "surname", "patronymic"]
        labels = {
            "name": "Ім'я",
            "surname": "Прізвище",
            "patronymic": "По батькові",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Введіть ім'я"}),
            "surname": forms.TextInput(attrs={"class": "form-control", "placeholder": "Введіть прізвище"}),
            "patronymic": forms.TextInput(attrs={"class": "form-control", "placeholder": "Введіть по батькові"}),
        }
        