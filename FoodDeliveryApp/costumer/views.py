from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.core.mail import send_mail
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
import sqlite3
from .models import MenuItem, Category, OrderModel,Orderrs,OrderItem
from django.shortcuts import render
from django.urls import reverse_lazy
from django.db.models import Q
import json
import datetime
from django.db.models import Prefetch


from django.contrib.auth.decorators import login_required

from.forms import CreateUserForm

class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'costumer/index.html')


class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'costumer/about.html')



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


def menu(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        orderrs ,created = Orderrs.objects.get_or_create(customer=customer, complete=False)
        products = orderrs.orderitem_set.all()
        cartItems = orderrs.get_cart_products
    else:
        products = []
        orderrs = {'get_cart_total': 0, 'get_cart_products': 0, 'shipping': False}
        cartItems = orderrs['get_cart_products']

    categories = Category.objects.prefetch_related(Prefetch('item', queryset=MenuItem.objects.all().order_by('name')))
    context = {'categories': categories, 'cartItems': cartItems}
    return render(request, 'costumer/menu.html', context)


class Menusearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("q")

        menu_items=MenuItem.objects.filter(
            Q(name__icontains=query)|
            Q(price__icontains=query)|
            Q(description__icontains=query)
        )

        context = {
            'menu_items':menu_items
        }

        return render(request,'costumer/menu.html',context)

def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        orderrs ,created = Orderrs.objects.get_or_create(customer=customer,complete=False)
        products = orderrs.orderitem_set.all()
        cartItems=orderrs.get_cart_products
    else:
        products=[]
        orderrs={'get_cart_total':0,'get_cart_products':0,'shipping':False}
        cartItems = orderrs['get_cart_products']

    context={'products':products,'orderrs':orderrs,'cartItems':cartItems}
    return render(request,'costumer/cart.html',context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        orderrs ,created = Orderrs.objects.get_or_create(customer=customer,complete=False)
        products = orderrs.orderitem_set.all()
        cartItems = orderrs.get_cart_products
    else:
        products=[]
        orderrs={'get_cart_total':0,'get_cart_products':0,'shipping':False}
        cartItems = orderrs['get_cart_products']

    context={'products':products,'orderrs':orderrs,'cartItems':cartItems}
    return render(request,'costumer/checkout.html',context)


def update_item(request):
    data = json.loads(request.body)
    itemId = data['itemId']
    action = data['action']
    print('Action:', action)
    print('itemId:', itemId)

    customer = request.user.customer
    item=MenuItem.objects.get(id=itemId)
    orderrs, created = Orderrs.objects.get_or_create(customer=customer, complete=False)
    orderrsItem , created = OrderItem.objects.get_or_create(orderrs=orderrs,item=item)

    if action == 'add':
        orderrsItem.quantity=(orderrsItem.quantity + 1)
    elif action =='remove':
        orderrsItem.quantity = (orderrsItem.quantity - 1)

    orderrsItem.save()

    if orderrsItem.quantity <= 0:
        orderrsItem.delete()

    return JsonResponse('Item was added', safe=False)

def processorder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        orderrs, created = Orderrs.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        orderrs.transaction_id = transaction_id

        if total == float(orderrs.get_cart_total):
            orderrs.complete = True
        orderrs.save()

        if orderrs.shipping == True:
            OrderModel.objects.create(
                customer=customer,
                orderrs=orderrs,
                street=data['shipping']['street'],
                city = data['shipping']['city'],

            )

    else:
        print('User is not logged in...')
        return render(request,'costumer/login.html')

    return JsonResponse('Very Good', safe=False)



