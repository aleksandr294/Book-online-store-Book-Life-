from django import forms
from .models import Comment, Order
from captcha.fields import CaptchaField
class CommentForm(forms.ModelForm):
    name= forms.CharField(label ='', widget= forms.TextInput(attrs={'class': 'form-control',  'style': 'width: 250px;', 'placeholder': 'Введите ваше имя'}))
    email= forms.EmailField(label ='', widget= forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 250px;', 'placeholder': 'Введите ваш email'}))
    body= forms.CharField(label ='', widget= forms.Textarea(attrs={'class': 'form-control', 'style': 'width: 500px;', 'placeholder': 'Введите ваш комментарий'}))
    captcha = CaptchaField(label='Введите текст с картинки', error_messages={'invalid': 'Неправильный текст'})
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body', 'captcha')



BOOK_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]
class CartAddBookForm(forms.Form):
    #quantity = forms.IntegerField()
    quantity = forms.TypedChoiceField(choices=BOOK_QUANTITY_CHOICES, coerce=int, label='Количество')
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

class OrderCreateForm(forms.ModelForm):
    first_name= forms.CharField(label ='Имя', widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваше имя'}))
    last_name= forms.CharField(label ='Фамилия', widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите вашу фамилию'}))
    email = forms.EmailField(label ='Email', widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    address = forms.CharField(label ='Адрес', widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваш адрес'}))
    postal_code = forms.CharField(label ='Почтовый индекс', widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваш почтовый индекс'}))
    city = forms.CharField(label ='Город', widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваш город'}))
    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'address', 'postal_code', 'city')

class SearchForm(forms.Form):
    query = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control mr-sm-2',  'type': 'search', 'placeholder': 'Search', 'aria-label':'Search'}))


class LoginForm(forms.Form):
    userName = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)