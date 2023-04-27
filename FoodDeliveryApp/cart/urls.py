from django.urls import path
from . import views

app_name = ' cart'

urlpatterns = [
    path('',views.cart_detail,name='cart_detail'),
    path('add/<int:item_id>/',views.cart_add,name='cart_add'),
    path('remove/<int:item_id>/', views.cart_remove, name='remove_item'),
]