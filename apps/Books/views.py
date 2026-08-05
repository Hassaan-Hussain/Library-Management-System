from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Books, BorrowedBook
from .forms import AddBookForm, BorrowBookForm
from django.contrib import messages
from django.contrib.auth.models import User

  
# Books Display View

def book_display_view(request):
    try:
        books = Books.objects.all()
        borrowed_books = BorrowedBook.objects.filter(user=request.user.id)
    except Exception as e:
        raise e

    print(request.user)
    return render(
        request, 
        'Books/books_display.html', 
        {
            'books': books,
            'borrowed_books': borrowed_books,
        }
    )

# Books Adding View
@login_required(login_url='login')
def book_add_view(request):
    if request.method == 'POST':
        form = AddBookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request,'Book successfully added')
            return redirect('books_view')
    else:
        form = AddBookForm()

    return render(request, 'Books/add_books.html', {'form': form})

# Books Deleting View
@login_required(login_url='login')
def delete_book_view(request, id):
    book = get_object_or_404(Books, pk=id)
    book.delete()
    return redirect('books_view')

# Update Book View
@login_required(login_url='login')
def update_book_view(request, id):
    book = get_object_or_404(Books, pk=id)

    if request.method == 'POST':
        form = AddBookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('books_view')
    else:
        form = AddBookForm(instance=book)
        
    return render(request, 'Books/update_book.html', {'book': form})

# Borrow Book View
@login_required(login_url='login')
def borrow_book_view(request, id):
    user = get_object_or_404(User, pk=request.user.id)
    book_id = id
    book = get_object_or_404(Books, pk=id)

    if request.method == 'POST':
        form = BorrowBookForm(request.POST)
        if form.is_valid():
            book_borrower = form.save(commit=False)
            book_borrower.user = user
            book_borrower.book = book
            book.quantity = book.quantity - book_borrower.no_of_books
            book.save()
            book_borrower.save()
            messages.success(request, 'Book Borrowed')            
            return redirect('books_view')
    else:
        form = BorrowBookForm()

    return render(
        request, 
        'Books/borrow_book.html', 
        {
        'form': form,
        'book': book
        }
        )