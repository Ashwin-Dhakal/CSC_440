def cart_item_count(request):
    cart = request.session.get('cart', {})
    count = 0
    if isinstance(cart, dict):
        for quantity in cart.values():
            try:
                amount = int(quantity)
            except (TypeError, ValueError):
                continue
            if amount > 0:
                count += amount
    return {'cart_count': count}
