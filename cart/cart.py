from django.conf import settings
from product.models import Product


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def __iter__(self):
        for p in self.cart.keys():
            # Fetch the product for each item in the cart
            self.cart[p]['product'] = Product.objects.get(pk=p)
            # Calculate the total price for each item
            self.cart[p]['total_price'] = int(self.cart[p]['product'].price * self.cart[p]['quantity']) / 100
            yield self.cart[p]

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def add(self, product_id, quantity=1, update_quantity=False):
        product_id = str(product_id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'id': product_id}

        if update_quantity:
            self.cart[product_id]['quantity'] = int(quantity)
        else:
            self.cart[product_id]['quantity'] += int(quantity)

        if self.cart[product_id]['quantity'] <= 0:
            self.remove(product_id)

        self.save()

    def remove(self, product_id):
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
            
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def get_total(self):
        for p in self.cart.keys():
            # Fetch the product for each item in the cart
            self.cart[p]['product'] = Product.objects.get(pk=p)
        return int(sum(item['product'].price * item['quantity'] for item in self.cart.values())) / 100
    

    def get_item(self, product_id):
        if str(product_id) in self.cart:
             return self.cart[str(product_id)] 
        else:
            return None

