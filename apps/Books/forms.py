from .models import Books, BorrowedBook
from django import forms
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError

class AddBookForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = '__all__'

class BorrowBookForm(forms.ModelForm):
    class Meta:
        model = BorrowedBook
        fields = ['no_of_books', 'return_date']

        widgets = {
            'no_of_books': forms.NumberInput(attrs={
             'max': '3', 
             'min':'1',
             }),

             'return_date': forms.DateInput(attrs={
                 'type': 'date',
             })
        }

        help_texts = {
            'no_of_books': '1000 fee per book, lease allowed for 3 books max',
            'return_date': 'Return within 1 Month to avoid fine',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        today = timezone.now()
        one_month = today + timedelta(days=30)

        self.fields['return_date'].widget.attrs['min'] = today.strftime('%Y-%m-%d')
        self.fields['return_date'].widget.attrs['max'] = one_month.strftime('%Y-%m-%d')
        

    def clean_return_date(self):
        return_date = self.cleaned_data.get('return_date')
        return_date = self.cleaned_data.get('return_date')
        today = timezone.now()
        one_month_later = today + timedelta(days=30)

        if return_date:
            if return_date < today:
                raise ValidationError('Return date cannot be in the past')
            if return_date > one_month_later:
                raise ValidationError('Return Date cannot be more than 30 days')

        return return_date