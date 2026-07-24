from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Books(models.Model):
    name = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    quantity = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Books'

    def __str__(self):
        return self.name
    
class BorrowedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    no_of_books = models.IntegerField(validators=[
        MaxValueValidator(3),
        MinValueValidator(1),
    ])
    fee = models.IntegerField()
    borrowed_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'book'], name='my_constraint'
            )
        ]

    def __str__(self):
        return f"{self.user}:  '{self.book}'"

    def save(self, *args, **kwargs):
        for _ in range(self.no_of_books):
            self.fee = self.no_of_books * 1000

        self.full_clean()
        super().save(*args, **kwargs)