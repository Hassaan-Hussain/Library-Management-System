from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_display_view, name='books_view'),
    path('add/', views.book_add_view, name='add_book'),
    path('delete/<int:id>/', views.delete_book_view, name='delete_book'),
    path('update/<int:id>/', views.update_book_view, name='update_book'),
]
