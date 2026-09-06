from django.contrib import admin
from .models import Books, BorrowedBook

# Register your models here.

class BorrowedBookAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'no_of_books', 'fee', 'return_date', 'borrowed_date', 'days_remaining']
    list_display_links = ['user']


admin.site.register(Books)
admin.site.register(BorrowedBook, BorrowedBookAdmin)
