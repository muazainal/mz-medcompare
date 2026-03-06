def cart_count(request):
    """
    Context processor that returns the total count of items in the cart
    available to all templates.
    """
    cart = request.session.get('cart', {})
    count = sum(cart.values())
    return {'cart_count': count}
