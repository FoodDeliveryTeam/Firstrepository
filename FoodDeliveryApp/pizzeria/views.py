from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from datetime import datetime
from costumer.models import OrderModel,Customer



class Dashboard(LoginRequiredMixin, UserPassesTestMixin, View):

    def get(self, request, *args, **kwargs):

        today = datetime.today()
        orders = OrderModel.objects.filter(created_on__year=today.year,created_on__month=today.month,created_on__day=today.day)

        customers = [order.customer for order in orders]

        total_revenue = 0
        for order in orders:
            total_revenue += order.orderrs.get_cart_total

        context = {
            'orders': orders,
            'total_revenue': total_revenue,
            'total_orders': len(orders),
            'customers': customers,
        }
        return render(request, 'pizzeria/dashboard.html', context)

    def test_func(self):
        return self.request.user.groups.filter(name='Staff').exists()



