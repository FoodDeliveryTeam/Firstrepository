from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import MenuItem, Category, OrderModel,Orderrs,OrderItem,Customer

admin.site.register(MenuItem)
admin.site.register(Category)
admin.site.register(OrderModel)
admin.site.register(Customer)
admin.site.register(Orderrs)
admin.site.register(OrderItem)


def image_show(self,obj):
    if obj.image:
        return mark_safe("<img src='{{ item.image }}' width='60' />",format(obj.image.url))
    return "None"

image_show.__name__="Картинка"
# Register your models here.
