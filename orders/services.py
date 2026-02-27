from cart.models import Cart, CartItem
from orders.models import OrderItem


class OrderConfirmationError(Exception):
    pass


def check_user_cart(cart):
    if cart is None:
        raise OrderConfirmationError("Cart does not exist")
    cart_items = CartItem.objects.filter(cart=cart)
    if len(cart_items) == 0:
        raise OrderConfirmationError("Cart is empty")
    else:
        for item in cart_items:
            book = item.book
            if book.quantity < 1 or book.quantity < item.quantity:
                raise OrderConfirmationError("Not enough books")
    return cart_items


def fill_order(order, cart_items):
    for item in cart_items:
        book = item.book
        price = item.price
        quantity = item.quantity
        order_item = OrderItem.objects.create(order=order, item=book, price=price, quantity=quantity)
        book.quantity -= item.quantity
        book.save()
        order.total_price += price * quantity
        order_item.save()
        order.save()
