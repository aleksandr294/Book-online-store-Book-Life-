from django.contrib import admin
from .models import Books
from .models import Genre
from .models import Author
from .models import BookPages
from .models import Comment
from .models import Order
from .models import OrderItem
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ['nameBook', 'author', 'genre', 'published', 'language', 'pages']
    list_filter = ('genre', 'author')
    search_fields = ['nameBook', 'author', 'genre']
    class Meta:
        model = Books

class GenreAdmin(admin.ModelAdmin):
    list_display = ['genre']
    class Meta:
        model = Genre

class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name_author']
    class Meta:
        model = Author

class BookPagesAdmin(admin.ModelAdmin):
    list_display = ['nameBook', 'pageBook']
    class Meta:
        model = BookPages

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'book', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['book']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email','address', 'postal_code', 'city', 'paid', 'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]

admin.site.register(Books, PostAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(BookPages, BookPagesAdmin)
admin.site.register(Comment, CommentAdmin)