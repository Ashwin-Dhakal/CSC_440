from decimal import Decimal

from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Product

# Customers may order between 1 and 20 units of a single product.
MAX_CART_QUANTITY = 20


def _session_cart(request):
    """Return a mutable copy of the session cart, or {} if missing/invalid."""
    cart = request.session.get('cart', {})
    if not isinstance(cart, dict):
        return {}
    return dict(cart)


def _positive_quantity(value):
    """Parse a cart quantity. Return an int in 1..MAX_CART_QUANTITY, or None."""
    try:
        quantity = int(value)
    except (TypeError, ValueError):
        return None
    if quantity < 1 or quantity > MAX_CART_QUANTITY:
        return None
    return quantity


def menu_list(request):
    products = Product.objects.all()
    return render(request, 'menu.html', {'products': products})


@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = _session_cart(request)
    product_key = str(product.pk)
    current = _positive_quantity(cart.get(product_key)) or 0
    if current >= MAX_CART_QUANTITY:
        return redirect('menu_list')
    cart[product_key] = current + 1
    request.session['cart'] = cart
    return redirect('menu_list')


@require_POST
def cart_increase(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = _session_cart(request)
    product_key = str(product.pk)
    current = _positive_quantity(cart.get(product_key))
    if current is None:
        # Not in cart, or corrupt/non-positive value: do not invent a bad entry.
        # Drop a corrupt key if present; leave absent keys alone.
        if product_key in cart:
            del cart[product_key]
            request.session['cart'] = cart
        return redirect('cart_detail')
    if current >= MAX_CART_QUANTITY:
        return redirect('cart_detail')
    cart[product_key] = current + 1
    request.session['cart'] = cart
    return redirect('cart_detail')


@require_POST
def cart_decrease(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = _session_cart(request)
    product_key = str(product.pk)
    current = _positive_quantity(cart.get(product_key))
    if current is None:
        if product_key in cart:
            del cart[product_key]
            request.session['cart'] = cart
        return redirect('cart_detail')
    if current == 1:
        del cart[product_key]
    else:
        cart[product_key] = current - 1
    request.session['cart'] = cart
    return redirect('cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = _session_cart(request)
    product_key = str(product_id)
    if product_key in cart:
        del cart[product_key]
        request.session['cart'] = cart
    return redirect('cart_detail')


@require_POST
def cart_update(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = _session_cart(request)
    product_key = str(product.pk)
    if product_key not in cart:
        return redirect('cart_detail')
    quantity = _positive_quantity(request.POST.get('quantity'))
    if quantity is None:
        return redirect('cart_detail')
    cart[product_key] = quantity
    request.session['cart'] = cart
    return redirect('cart_detail')


def cart_detail(request):
    session_cart = _session_cart(request)
    product_ids = []
    for product_key in session_cart:
        try:
            product_ids.append(int(product_key))
        except (TypeError, ValueError):
            continue

    products = Product.objects.in_bulk(product_ids)
    lines = []
    total = Decimal('0.00')
    for product_key, quantity in session_cart.items():
        try:
            product = products.get(int(product_key))
        except (TypeError, ValueError):
            continue
        quantity = _positive_quantity(quantity)
        if product is None or quantity is None:
            continue
        line_total = (product.price * quantity).quantize(Decimal('0.01'))
        total += line_total
        lines.append({
            'product_id': product.pk,
            'name': product.name,
            'image_url': product.image_url,
            'price': product.price,
            'quantity': quantity,
            'line_total': line_total,
        })

    return render(request, 'cart.html', {
        'lines': lines,
        'total': total,
    })
