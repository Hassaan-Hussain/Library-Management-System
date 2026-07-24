from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib import messages

# Create your models here.

class Books(models.Model):
    name = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    quantity = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Books'
        # permissions = [
        #     ('add_book', 'Hassaan can add book'),
        # ]

    def __str__(self):
        return self.name
    
class BorrowedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    borrowed_date = models.DateTimeField(auto_now_add=True)
    # return_date = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'book'], name='my_constraint'
            )
        ]

    def __str__(self):
        return f"{self.user}:  '{self.book}'"
    
    