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


def merge_carts(request, user):
    session_id = request.session.session_key
    anonymous_cart = Cart.objects.filter(customer=None, session_id=session_id).first()
    user_cart = Cart.objects.filter(customer=user, session_id=None).first()
    if anonymous_cart:
        if user_cart:
            #CartItem.objects.filter(cart_id=anonymous_cart.id).update(cart_id=user_cart.id)
            anonymous_items = CartItem.objects.filter(cart=anonymous_cart.id)
            user_items = CartItem.objects.filter(cart=user_cart.id)
            for anonymous_item in anonymous_items:
                for user_item in user_items:
                    if anonymous_item.book == user_item.book:
                        user_item.quantity += anonymous_item.quantity

                    else:
                        anonymous_item.cart_id = user_cart.id
                    user_item.save()
            anonymous_cart.delete()
        else:
            anonymous_cart.session_id = None
            anonymous_cart.customer = user
            anonymous_cart.save()
    else:
        return

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


