from django.db import models


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='menu_images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ManyToManyField('Category', related_name='item')

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class OrderModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    items = models.ManyToManyField('MenuItem', related_name='order', blank=True)
    name= models.CharField(max_length=70,blank=True)
    email = models.CharField(max_length=70,blank=True)
    street =  models.CharField(max_length= 70,blank = True)
    city = models.CharField(max_length=70,blank = True)



    def __str__(self):
        return f'Order: {self.created_on.strftime("%b %d %I: %M %p")}'