from django.shortcuts import render,redirect
from django.views import View
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
import sqlite3
from .models import MenuItem, Category, OrderModel
from django.shortcuts import render
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required

from.forms import CreateUserForm


class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'costumer/index.html')


class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'costumer/about.html')


class Order(View):
    def get(self, request, *args, **kwargs):
        # get every item from each category
        appetizers = MenuItem.objects.filter(category__name__contains='Appetizer')
        pizzas = MenuItem.objects.filter(category__name__contains='Pizza')
        desserts = MenuItem.objects.filter(category__name__contains='Dessert')
        drinks = MenuItem.objects.filter(category__name__contains='Drink')

        # pass into context
        context = {
            'appetizers': appetizers,
            'pizzas': pizzas,
            'desserts': desserts,
            'drinks': drinks,
        }

        # render the template
        return render(request, 'costumer/order.html', context)

    def post(self, request, *args, **kwargs):
        name=request.POST.get('name')
        email=request.POST.get('email')
        street=request.POST.get('street')
        city=request.POST.get('city')


        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }

            order_items['items'].append(item_data)

        price = 0
        item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])

        order = OrderModel.objects.create(price=price,name=name,email=email,street=street,city=city)
        order.items.add(*item_ids)

        #отпрвить сообщение на почту или смс
        body=('Спасибо за заказ!Ваш заказ будет готов с минуты на минуту и будет доставлен наибыстрейшим способом!\n'
              f'Итоговая цена : {price}\n'
              'Спасибо за заказ ! Заказывайте еще!')

        send_mail(
            'Спасибо за заказ!',
            body,
            'project@gmail.com',
            [email],
            fail_silently=False
        )

        context = {
            'items': order_items['items'],
            'price': price
        }

        return render(request, 'costumer/order_confirmation.html', context)


def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form=CreateUserForm
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user=form.cleaned_data.get('username')
                messages.success(request,'Аккаунт был создан ' + user)
                return redirect('login')

        context = {'form' : form}
        return render(request,'accounts/register.html',context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.info(request,"Пароль или имя пользователя не верны ")

        context = {}
        return render(request, 'accounts/login.html', context)

def logoutuser(request):
    logout(request)
    return redirect('login')

