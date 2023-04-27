from django.conf import settings
from decimal import Decimal
from costumer.models import MenuItem




class Cart(object):
    def __init__(self,request):
        self.session=request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart=self.session[settings.CART_SESSION_ID] = {}

        self.cart=cart

        def __iter__(self):
            item_ids=self.cart.keys()
            items = MenuItem.objects.filter(id__in=item_ids)

            cart = self.cart.copy()
            for item in items:
                cart[str(item.id)]['item']=item

            for product in cart.values():
                product['price'] = Decimal(product['price'])
                product['total_price']=product['price'] * product['quantity']
                yield product



        def __len__(self):
            return sum(product['quantity'] for product in self.cart.values())


        def add(self, item, quantity=1, update_quantity=False):
            item_id=str(item.id)

            if item_id not in self.cart:
                self.cart[item_id] = {'quantity':0,'price':str(item.price)}

            if update_quantity:
                self.cart[item_id]['quantity'] = quantity
            else:
                self.cart[item_id]['quantity'] += quantity
            self.save()

        def save(self):
            self.session.modified=True

        def remove(self,item_):
            item_id=str(item.id)
            if item_id in self.cart:
                del self.cart[item_id]
                self.save()

        def total_price(self):
            return sum(Decimal(product['price']) * product['quantity'] for product in self.cart.values())

        def clear(self):
            del self.session[settings.CART_SESSION_ID]
            self.save()





