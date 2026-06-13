from django import forms
from .models import Order
from book.models import Book

# Кастомне поле для гарного виводу назви книги в списку замовлення
class CustomBookChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.name} (В наявності: {obj.count} шт.)"

class OrderForm(forms.ModelForm):

    book = CustomBookChoiceField(
        queryset=Book.objects.filter(count__gt=0), 
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Оберіть книгу"
    )
    
    plated_end_at = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            "class": "form-control", 
            "type": "datetime-local" 
        }),
        label="Планована дата повернення"
    )

    class Meta:
        model = Order
        fields = ["book", "plated_end_at"]
