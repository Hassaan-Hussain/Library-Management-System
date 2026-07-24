from .models import Books
from django import forms

class AddBookForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = '__all__'