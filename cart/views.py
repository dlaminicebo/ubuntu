from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .cart import Cart
from product.models import Product

# Create your views here.

def add_to_cart(request, product_id):
    cart = Cart(request)
    cart.add(product_id)
    return render(request, 'cart/menu_cart.html')  # Corrected the template name

def cart(request):
    return render(request, 'cart/cart.html')

def success(request):
    return render(request, 'cart/success.html')

def update_cart(request, product_id, action): # This function is for increasing/decreasing product quantity
    cart = Cart(request)

    if action == 'increment':
        cart.add(product_id, 1, True)
    else:
        cart.add(product_id, -1, True)

    product = Product.objects.get(pk=product_id)
    quantity = cart.get_item(product_id)

    if quantity:
        # You seem to have a typo here. I corrected it to access the quantity correctly.
        quantity = quantity['quantity']  # Changed quantity[quantity] to quantity['quantity']
        item = {
            'product': {
                'id': product.id,
                'name': product.name,
                'image': product.get_thumbnail(),
                'price': product.price,
            },
            'total_price': (quantity * product.price) / 100,
            'quantity': quantity,
        }
    else:
        item = None

    response = render(request, 'cart/partials/cart_item.html', {'item': item})
    response['HX-Trigger'] = 'update-menu-cart'

    return response

@login_required
def checkout(request):
    return render(request, 'cart/checkout.html')

def hx_menu_cart(request):
    return render(request, 'cart/menu_cart.html')

def hx_cart_total(request):
    return render(request, 'cart/partials/cart_total.html')

def hx_cart_total(request):
    return render(request, 'cart/partials/cart_total.html')

def trackOrder(request):
    return render(request, 'cart/trackOrder.html')

def order_details(request):
    return render(request, 'cart/order_details.html')

def size(request):
    return render(request, 'cart/size.html')

def scan(request):
    return render(request, 'cart/scan.html')

def map(request):
    return render(request, 'cart/map.html')