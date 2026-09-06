from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Sum, Avg, Max, Min, Count
from app.forms import BookForm
from app.models import Book

def welcome(request):
    total_books = Book.objects.count()
    total_value = Book.objects.aggregate(Sum('price'))['price__sum'] or 0
    genres_count = Book.objects.values('genre').distinct().count()
    recent_books = Book.objects.order_by('-id')[:6]
    
    context = {
        'total_books': total_books,
        'total_value': total_value,
        'genres_count': genres_count,
        'recent_books': recent_books,
    }
    return render(request, 'index.html', context)

def admin_dashboard(request):
    total_books = Book.objects.count()
    aggregates = Book.objects.aggregate(
        total_val=Sum('price'),
        avg_price=Avg('price'),
        max_price=Max('price'),
        min_price=Min('price')
    )
    total_value = aggregates['total_val'] or 0
    avg_price = aggregates['avg_price'] or 0
    
    highest_book = Book.objects.order_by('-price').first()
    lowest_book = Book.objects.order_by('price').first()

    genre_stats_qs = Book.objects.values('genre').annotate(count=Count('id')).order_by('-count')
    
    genre_stats = []
    for item in genre_stats_qs:
        genre_name = item['genre'] or 'Uncategorized'
        count = item['count']
        percentage = round((count / total_books * 100), 1) if total_books > 0 else 0
        genre_stats.append({
            'name': genre_name,
            'count': count,
            'percentage': percentage
        })

    recent_books = Book.objects.order_by('-id')[:8]

    context = {
        'total_books': total_books,
        'total_value': total_value,
        'avg_price': avg_price,
        'highest_book': highest_book,
        'lowest_book': lowest_book,
        'genre_stats': genre_stats,
        'recent_books': recent_books,
    }
    return render(request, 'admin_dashboard.html', context)

def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            messages.success(request, f"Book '{book.title}' added successfully!")
            return redirect('get_all_books')
        else:
            messages.error(request, "Failed to add book. Please check the form errors below.")
    else:
        form = BookForm()
    
    return render(request, "add_book.html", {"form": form})

def get_all_books(request):
    query = request.GET.get('q', '').strip()
    genre_filter = request.GET.get('genre', '').strip()
    sort_by = request.GET.get('sort', '').strip()

    books = Book.objects.all()

    if query:
        books = books.filter(
            Q(title__icontains=query) | 
            Q(author__icontains=query) | 
            Q(isbn__icontains=query)
        )

    if genre_filter:
        books = books.filter(genre__iexact=genre_filter)

    if sort_by == 'price_asc':
        books = books.order_by('price')
    elif sort_by == 'price_desc':
        books = books.order_by('-price')
    elif sort_by == 'title':
        books = books.order_by('title')
    else:
        books = books.order_by('-id')

    all_genres = Book.objects.values_list('genre', flat=True).distinct()
    all_genres = [g for g in all_genres if g]

    context = {
        'books': books,
        'query': query,
        'genre_filter': genre_filter,
        'sort_by': sort_by,
        'all_genres': all_genres,
        'total_count': books.count(),
    }
    return render(request, "list.html", context)

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, "detail.html", {"book": book})

def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            updated_book = form.save()
            messages.success(request, f"Book '{updated_book.title}' updated successfully!")
            return redirect('book_detail', pk=book.pk)
        else:
            messages.error(request, "Failed to update book. Please check the inputs.")
    else:
        form = BookForm(instance=book)
    
    return render(request, "edit_book.html", {"form": form, "book": book})

def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        title = book.title
        book.delete()
        messages.success(request, f"Book '{title}' was deleted successfully.")
        return redirect('get_all_books')
    
    return render(request, "delete_confirm.html", {"book": book})


