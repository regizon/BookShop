from .models import Cart, CartItem


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


def get_book(serializer, cart):
    book = serializer.validated_data.get('book')
    price = book.price
    cart_item = CartItem.objects.filter(cart=cart, book=book).first()
    return price, cart_item