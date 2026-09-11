from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Books, BorrowedBook
from .forms import AddBookForm, BorrowBookForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.db import transaction
from django.utils import timezone
from django.core.paginator import Paginator
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string

  
# Books Display View

@login_required(login_url='login')
def book_display_view(request):

    html_message = render_to_string(
        'email/email.html',
    )
    send_mail(
        "Django Test Mail Feature",
        "Django Email Working",
        "hafizhassaan114@gmail.com",
        ["f2022105156@umt.edu.pk"],
        html_message=html_message,
    )







    # email.attach_alternative(
    #     "<h1>Hello Alternative</h1>"
    #     "<italic> New Message </italic>",
    #     "text/html"
    # )
    # email.send()



    sort_by = request.GET.get('sort')
    print(sort_by)

    allowed_sorted_fields = {
        'name': 'name',
        'author': 'author',
    }

    books = Books.objects.all()

    if sort_by == 'name':
        sort_by_field = allowed_sorted_fields.get(sort_by, 'name')
        books = Books.objects.all().order_by(sort_by_field)
        
    if sort_by == 'author':
        sort_by_field = allowed_sorted_fields.get(sort_by, 'author')
        books = Books.objects.all().order_by(sort_by_field)

    paginator = Paginator(books, 2)
    page_number = request.GET.get('page')
    books_page = paginator.get_page(page_number)

    
    borrowed_books = BorrowedBook.objects.filter(
        user=request.user,
        is_returned=False,
    )
    
    borrowed_books_history = BorrowedBook.objects.filter(
        user=request.user,
        is_returned=True,
    )
    borrowed_books_ids = borrowed_books.values_list('book_id', flat=True)

    # Fetching borrowed book ids to display Books borrowed or not
    # Fine penalty after due date
    for borrowed_book in borrowed_books:
        if (
            borrowed_book.return_date
            and borrowed_book.return_date.date() < timezone.localdate()
        ):
            borrowed_book.save(update_fields=['fee'])
    
    return render(
        request, 
        'Books/books_display.html', 
        {
            'books': books_page,
            'borrowed_books': borrowed_books,
            'borrowed_books_history': borrowed_books_history,
            'borrowed_books_ids': borrowed_books_ids,
            'sort': sort_by,
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
            try:
                book_borrower = form.save(commit=False)
                book_borrower.user = user
                book_borrower.book = book
                book.quantity = book.quantity - book_borrower.no_of_books
                book.save()
                book_borrower.save()
                send_mail(
                    "Django Test Mail Feature",
                    "Django Email Working",
                    "hafizhassaan114@gmail.com",
                    ["f2022105156@umt.edu.pk"],
                )
                messages.success(request, 'Book Borrowed')            
                return redirect('books_view')
            except:
                raise Exception
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

@login_required(login_url='login')
def return_book_view(request, id):
    borrowed_book = get_object_or_404(BorrowedBook, pk=id)

    if request.method == 'POST':
        total_books_return = borrowed_book.no_of_books
        with transaction.atomic():
            borrowed_book.book.quantity += total_books_return
            borrowed_book.book.save(update_fields=['quantity'])
            borrowed_book.is_returned = True
            borrowed_book.save()

        messages.info(request, 'Book Returned Sucessfully')
        return redirect('books_view')

    return render(
        request, 
        'Books/return_book.html',
        {
            'book': borrowed_book,
        }
    ) 

@login_required(login_url='login')
def search_book_view(request):
    borrowed_books_ids = BorrowedBook.objects.filter(
        user=request.user,
        is_returned=False,
    ).values_list('book_id', flat=True)
    
    if request.method == 'GET':
        searched_book = request.GET.get('book', '').strip()
        book = Books.objects.filter(name__icontains=searched_book)
        return render(
            request, 
            'Books/search_books.html', 
            {
                'book': (book), 
                'query':searched_book,
                'borrowed_books_ids': borrowed_books_ids,
            })

