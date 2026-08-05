from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from datetime import timedelta

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
    return_date = models.DateTimeField(blank=True, null=True)
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

    def clean(self):
        today = timezone.now()
        one_month_later = today + timedelta(days=30)

        if self.return_date:
            if self.return_date < today:
                raise ValidationError('Return date cannot be in the past')
            if self.return_date > one_month_later:
                raise ValidationError('Return Date cannot be more than 30 days')