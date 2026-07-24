from django.contrib import admin
from .models import Books, BorrowedBook

# Register your models here.

admin.site.register(Books)
admin.site.register(BorrowedBook)
