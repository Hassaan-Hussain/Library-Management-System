from .models import Books, BorrowedBook
from django import forms

class AddBookForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = '__all__'

class BorrowBookForm(forms.ModelForm):
    class Meta:
        model = BorrowedBook
        fields = ['no_of_books',]

        widgets = {
            'no_of_books': forms.NumberInput(attrs={
             'max': '3', 
             'min':'1',
             }),
        }

        help_texts = {
            'no_of_books': '1000 fee per book, lease allowed for 3 books max',
        }