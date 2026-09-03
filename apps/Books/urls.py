from django.urls import path
from . import views

urlpatterns = [
    # CRUD URLS 
    path('', views.book_display_view, name='books_view'),
    path('add/', views.book_add_view, name='add_book'),
    path('delete/<int:id>/', views.delete_book_view, name='delete_book'),
    path('update/<int:id>/', views.update_book_view, name='update_book'),
    # Search Book
    path('search-book/', views.search_book_view, name='search_book'),
    # Book Borrowing URL
    path('borrow_book/<int:id>', views.borrow_book_view, name='borrow_book'),
    # Book Returning URL
    path('return_book/<int:id>', views.return_book_view, name='return_book'),
]
