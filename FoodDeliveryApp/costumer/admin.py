from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import MenuItem, Category, OrderModel,Orderrs,OrderItem,Customer

admin.site.register(MenuItem)
admin.site.register(Category)
admin.site.register(OrderModel)
admin.site.register(Customer)
admin.site.register(Orderrs)
admin.site.register(OrderItem)



# Register your models here.
