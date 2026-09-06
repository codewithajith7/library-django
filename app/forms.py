from django import forms
from app.models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "genre", "isbn", "price", "cover"]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. The Great Gatsby'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. F. Scott Fitzgerald'}),
            'genre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Fiction, Science, Tech, History'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 978-0743273565'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00', 'step': '0.01'}),
            'cover': forms.FileInput(attrs={'class': 'form-control-file', 'accept': 'image/*', 'id': 'id_cover_input'}),
        }

