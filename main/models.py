from django.db import models

# Create your models here.
class Author(models.Model):
    name_author = models.CharField(max_length = 70, db_index = True, verbose_name = 'Автор')
    biography = models.TextField(verbose_name = 'Биография', null = True)
    photo = models.ImageField(verbose_name = 'Фото', null = True)
    dateOfBirth = models.DateField(verbose_name = 'Дата рождения', null = True)
    debut = models.TextField(verbose_name = 'Дебют', null = True)
    reaction = models.TextField(verbose_name = 'Реакция', null = True)
    def __str__(self):
        return self.name_author

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Genre(models.Model):
    image = models.ImageField(verbose_name = 'Картинка жанра')
    genre = models.CharField(max_length = 60, db_index = True, verbose_name = 'Жанр')

    def __str__(self):
        return self.genre

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['genre']
        
class BookPages(models.Model):
    nameBook = models.CharField(max_length=64, db_index = True, blank=True, null=True, default=None, verbose_name = 'Название книги')
    pageBook = models.FileField(verbose_name='Отрывок книги')
    def __str__(self):
        return self.nameBook

    class Meta:
        verbose_name = 'Страница книги'
        verbose_name_plural = 'Страницы книги'
        ordering = ['nameBook']

class Books(models.Model):
    image = models.ImageField(verbose_name = 'Облокжка книги')
    nameBook = models.CharField(max_length=64, db_index = True, blank=True, null=True, default=None, verbose_name = 'Название книги')
    author = models.ForeignKey('Author', null = True, on_delete = models.PROTECT, verbose_name = 'Автор')
    genre = models.ForeignKey('Genre', null = True, on_delete = models.PROTECT, verbose_name = 'Жанр')
    publishingHouse = models.CharField(max_length=64, blank=True, null=True, default=None, verbose_name = 'Издательсво')
    published = models.DateField(verbose_name = 'Год издательства')
    language = models.CharField(max_length=64, blank=True, null=True, default=None, verbose_name = 'Язык')
    pages = models.CharField(max_length=64, blank=True, null=True, default=None, verbose_name = 'Страниц')
    description = models.TextField(verbose_name = 'Текст')
    price = models.IntegerField(blank=True, null=True, default=None, verbose_name = 'Цена')
    is_active=models.BooleanField(default=True, verbose_name = 'В наличии')
    def __str__(self):
        return self.nameBook
        
    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

class Comment(models.Model):
    book = models.ForeignKey('Books', on_delete = models.PROTECT,  related_name='comments')
    name = models.CharField(max_length=80, verbose_name = 'Имя')
    email = models.EmailField(verbose_name = 'email')
    body = models.TextField(verbose_name = 'Тело комментария')
    created = models.DateTimeField(auto_now_add=True, verbose_name = 'Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name = 'Дата обновления')
    active = models.BooleanField(default=True, verbose_name = 'Показ')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('created',)

    def __str__(self):
        return 'Комментарий от {} на {}'.format(self.name, self.book)

class Order(models.Model):
    first_name = models.CharField(max_length=50, verbose_name = 'Имя')
    last_name = models.CharField(max_length=50, verbose_name = 'Фамилия')
    email = models.EmailField()
    address = models.CharField(max_length=250, verbose_name = 'Адрес')
    postal_code = models.CharField(max_length=20, verbose_name = 'Почтовый индекс')
    city = models.CharField(max_length=100, verbose_name = 'Город')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False, verbose_name = 'Оплачено')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('-created',)
    
    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name = 'Заказ')
    book = models.ForeignKey(Books, related_name='order_items', on_delete=models.CASCADE, verbose_name = 'Книга')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name = 'Цена')
    quantity = models.PositiveIntegerField(default = 1, verbose_name = 'Количество')

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity