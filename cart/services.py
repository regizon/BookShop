from .models import Cart, CartItem


class NotEnoughItemsInStock(Exception):
    pass


class NotSuchItemInCart(Exception):
    pass

def get_or_create_cart(request):
    if request.user.is_anonymous:
        session_id = request.session.session_key
        if session_id is None:
            request.session.create()
            session_id = request.session.session_key
        cart = Cart.objects.get_or_create(customer=None, session_id=session_id)[0]

    else:
        cart = Cart.objects.get_or_create(customer=request.user, session_id=None)[0]


    return cart


def get_cart(request):
    try:
        if request.user.is_anonymous:
            session_id = request.session.session_key
            if session_id is None:
                return None
            return Cart.objects.get(customer=None, session_id=session_id)
        else:
            return Cart.objects.get(customer=request.user, session_id=None)
    except Cart.DoesNotExist:
        return None



def minus_item(book, cart):
    cart_item = CartItem.objects.filter(cart=cart, book=book).first()

    if cart_item:
        price = book.price
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        elif cart_item.quantity == 1:
            cart_item.delete()

    else:
        raise NotSuchItemInCart("В корзині немає такого товару")

def add_item(cart, book):
    price = book.price
    quantity = book.quantity
    cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book, price=price)
    if quantity > 0:
        if created:
            cart_item.save()
        else:
            if cart_item.quantity + 1 <= quantity:
                cart_item.quantity += 1
                cart_item.save()
            else:
                raise NotEnoughItemsInStock("На складі не вистчає товару")

        return cart_item

    else:
        raise NotEnoughItemsInStock("На складі не вистчає товару")


