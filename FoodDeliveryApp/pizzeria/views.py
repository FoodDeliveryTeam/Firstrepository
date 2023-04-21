from django.shortcuts import render
from django.views import View
from django.utils.timezone import datetime
from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin
from costumer.models import OrderModel

#Эта страница доступно только сотрудникам пиццерии

class Dashboard(LoginRequiredMixin,UserPassesTestMixin,View):
    def get(self,request,*args,**kwargs):

        today = datetime.today()
        orders = OrderModel.objects.filter(created_on__year=today.year,created_on__month=today.month,created_on__day=today.day)

        total_revenue=0
        for order in orders:
            total_revenue +=order.price

        context = {
            'orders':orders,
            'total_revenue':total_revenue,
            'total_orders': len(orders)
        }
        return render(request,'pizzeria/dashboard.html',context)

    def test_func(self):
        return self.request.user.groups.filter(name = 'Staff').exists()


class OrderDetails(LoginRequiredMixin,UserPassesTestMixin,View):
    def get(self,request,pk,*args,**kwargs):
        order = OrderModel.objects.get(pk=pk)
        context = {
            'order':order,
        }

        return render(request,'pizzeria/order_details.html',context)

    def test_func(self):
        return self.request.user.groups.filter(name = 'Staff').exists()

# Create your views here.
