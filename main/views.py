from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.core.mail import send_mail
from django.urls import reverse_lazy
from .models import Books, Genre, Author, BookPages, Comment, OrderItem
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import BooksSerializer
from .forms import CommentForm, CartAddBookForm, OrderCreateForm, LoginForm
from .cart import Cart
# Create your views here.
import re

def book(request, book):
    book = Books.objects.get(nameBook = book)
    comments = book.comments.filter(active=True)
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.book = book
            # Save the comment to the database
            new_comment.save()
            return HttpResponseRedirect(request.path)
    else:
        comment_form = CommentForm()

    author = Author.objects.all()
    try:
        page = BookPages.objects.get(nameBook = book)
    except:
        page = None
    #current_book = Books.objects.get(pk = book_id)
    cart_book_form = CartAddBookForm()
    
    context = {'book': book, 'author': author, 'page': page, 'comments': comments, 'comment_form': comment_form, 'cart_book_form': cart_book_form}
    return render(request, 'book.html', context )

def catalog(request)-> 'render':
    genre = Genre.objects.all()
    context = {'genre': genre}
    return render(request, '1.html', context )

@api_view(['GET'])
def api_books(request)-> 'render':
    if request.method == 'GET':
        books = Books.objects.all()
        serializer = BooksSerializer(books, many = True)
        return Response(serializer.data)

@api_view(['GET'])
def api_books_author(request, author)-> 'render':
    if request.method == 'GET':
        books = Books.objects.filter(author = Author.objects.get(name_author = author))
        serializer = BooksSerializer(books, many = True)
        return Response(serializer.data)

@api_view(['GET'])
def api_books_genre(request, genre)-> 'render':
    if request.method == 'GET':
        books = Books.objects.filter(genre = Genre.objects.get(genre = genre))
        serializer = BooksSerializer(books, many = True)
        return Response(serializer.data)

def by_author(request, author_id) -> 'render':
    books = Books.objects.filter(author = author_id)
    author = Author.objects.all()
    current_author = Author.objects.get(pk = author_id)
    context = {'books': books, 'author': author, 'current_author': current_author}
    return render(request, 'by_author.html', context )

def by_genre(request, genre_id) -> 'render':
    books = Books.objects.filter(genre = genre_id)
    genre = Genre.objects.all()
    current_genre = Genre.objects.get(pk = genre_id)
    context = {'books': books, 'genre': genre, 'current_genre': current_genre}
    return render(request, 'by_genre.html', context )

def index(request) -> 'render':
    #form = SearchForm()
    books = Books.objects.filter(is_active=True)
    paginator = Paginator(books, 8)
    genre = Genre.objects.all()
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
    
    index = books.number - 1 
    max_index = len(paginator.page_range)
    start_index = index - 3 if index >= 3 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index
    page_range = list(paginator.page_range)[start_index:end_index]

    
    

    context = {'books': books, 'genre': genre, 'page_range': page_range}
    return render(request, 'index.html', context)

@require_POST
def cart_add(request, book_id):
    cart = Cart(request)
    book = Books.objects.get(id=book_id)
    print('df',book)
    form = CartAddBookForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(book=book,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart')

def cart_remove(request, book_id):
    cart = Cart(request)
    book = Books.objects.get(id=book_id)
    cart.remove(book)
    return redirect('cart')

def cart(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddBookForm( initial={'quantity': item['quantity'], 'update': True})
    return render(request, 'detail.html', {'cart': cart})

def product_detail(request, id):
    book = Books.objects.get(id= id)
    cart_book_form = CartAddBookForm()
    return render(request, 'cart.html', {'book': book, 'cart_book_form': cart_book_form})

def order(request):
    cart = Cart(request)
    message = 'Спасибо за ваш заказ\n'
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            order = form.save()
            message += 'Заказ № {} \n'.format(order.id)
            for item in cart:
                message += 'Книга - {}, цена за единицу - {}₴, количество - {} \n'.format(item['book'], item['price'], item['quantity'])
                OrderItem.objects.create(order = order, book = item['book'], price = item['price'], quantity=item['quantity'])
            message += 'Итого {}₴'.format(cart.get_total_price())
            
            cart.clear()
            send_mail('Спасибо за ваш заказ у «Книжный интернет-магазин «BookLife»»', message, 'messer294@gmail.com', [email])
            return render(request, 'created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'create.html', {'cart': cart, 'form': form})
    #return render(request, 'created.html')

def search(request):
    search = request.GET.get('search', '')
    books = []
    count = 0
    if search:
        try:
            books = Books.objects.filter(author = Author.objects.get(name_author = search))
        except Author.DoesNotExist:
            #books = Books.objects.filter(nameBook = search)
            allBooks = Books.objects.all()
            for book in allBooks:
                if re.search(search, book.nameBook):
                    books.append(book)
        count = len(books)
    return render(request, 'search.html', {'books': books,  'search': search, 'count': count})



    

