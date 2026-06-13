from django import forms
from .models import Book
from author.models import Author

class CustomAuthorChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        # Гарне відображення ПІБ у списку
        return f"{obj.surname} {obj.name} {obj.patronymic}"

class BookForm(forms.ModelForm):
    authors = CustomAuthorChoiceField(
        queryset=Author.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "form-control"}),
        label="Автори (можна обрати кількох)"
    )

    class Meta:
        model = Book
        fields = ["name", "description", "count", "authors"]
        labels = {
            "name": "Назва книги",
            "description": "Опис / Анотація",
            "count": "Кількість примірників",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Введіть назву книги"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Додайте опис..."}),
            "count": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
        }
