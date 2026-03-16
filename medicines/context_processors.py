def cart_count(request):
    """
    Context processor that returns the total count of items in the cart
    available to all templates.
    """
    cart = request.session.get('cart', {})
    try:
        count = sum(int(v) for v in cart.values() if str(v).isdigit())
    except (TypeError, ValueError):
        count = 0
    return {'cart_count': count}
