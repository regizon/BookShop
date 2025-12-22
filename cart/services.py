from .models import Cart

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