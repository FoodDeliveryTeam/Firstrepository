from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=200,null=True)
    email=models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='menu_images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ManyToManyField('Category', related_name='item')
    digital = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.name



class Category(models.Model):
    name = models.CharField(max_length=100)


    def __str__(self):
        return self.name




class Orderrs(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    data_orderd=models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,blank=False)
    transaction_id=models.CharField(max_length=200,null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping =False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.item.digital == False:
                shipping =True
        return shipping

    @property
    def get_cart_total(self):
        orderitems =self.orderitem_set.all()
        total = sum([product.get_total for product in orderitems])
        return total

    @property
    def get_cart_products(self):
        orderitems = self.orderitem_set.all()
        total = sum([product.quantity for product in orderitems])
        return total


class OrderItem(models.Model):
    item=models.ForeignKey(MenuItem,on_delete=models.SET_NULL,blank=True,null=True)
    orderrs = models.ForeignKey(Orderrs,on_delete=models.SET_NULL,blank=True,null=True)
    quantity = models.IntegerField(default=0,null=True,blank = True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total= self.item.price * self.quantity
        return total


class OrderModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    orderrs = models.ForeignKey(Orderrs, on_delete=models.SET_NULL,blank=True,null=True)
    items = models.ManyToManyField('MenuItem', related_name='order', blank=True)
    name= models.CharField(max_length=70,blank=True)
    email = models.CharField(max_length=70,blank=True)
    street =  models.CharField(max_length= 70,blank = True)
    city = models.CharField(max_length=70,blank = True)


    def __str__(self):
        return self.street


