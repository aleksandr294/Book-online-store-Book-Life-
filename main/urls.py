"""BookLife URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import index, by_genre, catalog, by_author, book, cart, cart_add, cart_remove, order, search, api_books, api_books_author, api_books_genre
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('search/', search, name='search'),
    path('order/', order, name='order'),
    path('api/books/', api_books),
    path('api/books/author/<author>/', api_books_author),
    path('api/books/genre/<genre>/', api_books_genre),
    path('cart/', cart, name='cart'),
    path('add/<int:book_id>/', cart_add, name='cart_add'),
    path('remove/int:<book_id>/', cart_remove, name='cart_remove'),

    path('book/<book>/', book, name = 'book'),
    path('catalog/', catalog, name = 'catalog'),
    path('author/<int:author_id>/', by_author, name = 'by_author'),
    path('genre/<int:genre_id>/', by_genre, name = 'by_genre'),
    path('', index, name = 'index'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
