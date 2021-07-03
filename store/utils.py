import json
from .models import *

def cookie_cart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    print('Cart:', cart)
    items = []
    order = {'get_cart_total':0, 'get_cart_items':0}
    cart_items = order['get_cart_items']

    for id in cart:
        try:
            cart_items += cart[id]['quantity']

            product = Product.objects.get(id=id)
            total = (product.price * cart[id]['quantity'])
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[id]['quantity']

            item = {
                'product': {
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL
                },
                'quantity':cart[id]['quantity'],
                'get_total':total
            }
            items.append(item)
        except:
            pass
    return {'cart_items':cart_items, 'order':order, 'items':items}

def cookie_data(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items

    else:
        cookie_data = cookie_cart(request)
        items = cookie_data['items']
        cart_items = cookie_data['cart_items']
        order = cookie_data['order']
    
    return {'cart_items':cart_items, 'order':order, 'items':items}

def create_order(request, data):
    
    print('User is not logged in')

    print('COOKIES', request.COOKIES)
    name = data['form']['username']
    email = data['form']['useremail']

    cookies = cookie_cart(request)
    items = cookies['items']

    customer, created = Customer.objects.get_or_create(email=email,)
    customer.name = name
    customer.save()

    order = Order.objects.create(customer=customer, complete=False)

    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        order_item = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']

        )
    return customer, order