
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q

from .models import Item, Cart, Order, OrderItem
from .decorators import buyer_required
from seller.models import LocalItem, DealItem
from homemade.models import HomeMadeItem

@buyer_required
def buyer_home(request):
    query = request.GET.get('q', '')

    local_items = LocalItem.objects.filter(item__icontains=query)
    deal_items = DealItem.objects.filter(is_active=True, seller_item__item__icontains=query)
    homemade_items = HomeMadeItem.objects.filter(item__icontains=query)

    return render(request, 'buyer_home.html', {
        'local_items': local_items,
        'deal_items': deal_items,
        'homemade_items': homemade_items,
        'query': query,
    })

@buyer_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.subtotal for item in cart_items)
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })

@buyer_required
def update_cart_bulk(request):
    if request.method == 'POST':
        if 'increment' in request.POST:
            cart = Cart.objects.get(id=request.POST['increment'])
            cart.quantity += 1
            cart.save()
        elif 'decrement' in request.POST:
            cart = Cart.objects.get(id=request.POST['decrement'])
            if cart.quantity > 1:
                cart.quantity -= 1
                cart.save()
    return redirect('buyer:cart')

@buyer_required
def delete_from_cart(request, item_id):
    Cart.objects.filter(user=request.user, item__id=item_id).delete()
    return redirect('buyer:cart')

@buyer_required
def add_to_cart(request, item_id):
    item = get_object_or_404(HomeMadeItem, id=item_id)

    if item.order_count >= item.order_limit:
        messages.error(request, f"{item.item} is out of stock.")
        return redirect('buyer:buyer_home')

    cart_item, created = Cart.objects.get_or_create(user=request.user, item=item)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f"{item.item} added to cart.")
    return redirect('buyer:buyer_home')


@buyer_required
@require_http_methods(["GET", "POST"])
def checkout_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.subtotal for item in cart_items)

    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('buyer:cart')

    if request.method == 'POST':
        address_input = request.POST.get('delivery_address', '').strip()
        delivery_address = address_input or request.user.address

        # ✅ Check for limit violations before placing order
        for cart_item in cart_items:
            item = cart_item.item
            if isinstance(item, HomeMadeItem):
                if item.order_count + cart_item.quantity > item.order_limit:
                    messages.error(request, f"{item.item} is exceeds limit,Please decrease the quantity.")
                    return redirect('buyer:cart')

        order = Order.objects.create(
            user=request.user,
            total=total,
            delivery_address=delivery_address
        )

        for cart_item in cart_items:
            item = cart_item.item

            OrderItem.objects.create(
                order=order,
                item=item,
                quantity=cart_item.quantity,
                price=item.price
            )

            if isinstance(item, HomeMadeItem):
                item.order_count += cart_item.quantity
                item.save()

        cart_items.delete()

        subject = f"Order Confirmation - LocalBasket #{order.id}"
        message = f"""
Hi {request.user.first_name},

Your order (Order ID: {order.id}) has been successfully placed!
You ordered {order.items.count()} item(s) for a total of ₹{order.total}.

Delivery Address:
{delivery_address}

Thank you for shopping with LocalBasket!

- Team LocalBasket
"""
        try:
            send_mail(subject, message.strip(), settings.EMAIL_HOST_USER, [request.user.email])
        except Exception as e:
            print(f"Email failed: {e}")
            messages.warning(request, "Order placed, but confirmation email failed.")

        messages.success(request, "Your order has been placed!")
        return redirect('buyer:order_summary', order_id=order.id)

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total': total,
        'default_address': request.user.address
    })

@buyer_required
def place_order(request):
    if request.method == 'POST':
        cart_items = Cart.objects.filter(user=request.user)

        if not cart_items.exists():
            messages.error(request, "Your cart is empty.")
            return redirect('buyer:cart')

        total = sum(item.subtotal for item in cart_items)
        delivery_address = request.POST.get('delivery_address', '').strip()

        # ✅ Check for limit violations before placing order
        for cart_item in cart_items:
            item = cart_item.item
            if isinstance(item, HomeMadeItem):
                if item.order_count + cart_item.quantity > item.order_limit:
                    messages.error(request, f"{item.item} is out of stock or exceeds limit.")
                    return redirect('buyer:cart')

        order = Order.objects.create(
            user=request.user,
            total=total,
            delivery_address=delivery_address or None
        )

        for cart_item in cart_items:
            item = cart_item.item

            OrderItem.objects.create(
                order=order,
                item=item,
                quantity=cart_item.quantity,
                price=item.price
            )

            if isinstance(item, HomeMadeItem):
                item.order_count += cart_item.quantity
                item.save()

        cart_items.delete()

        subject = f"Order Confirmation - LocalBasket #{order.id}"
        message = f"""
Hi {request.user.first_name},

Your order (Order ID: {order.id}) has been successfully placed!
You ordered {order.items.count()} item(s) for a total of ₹{order.total}.

Delivery Address:
{delivery_address or 'Your default address'}

Thank you for shopping with LocalBasket!

- Team LocalBasket
"""
        try:
            send_mail(subject, message.strip(), settings.EMAIL_HOST_USER, [request.user.email])
        except Exception as e:
            print(f"Email failed: {e}")
            messages.warning(request, "Order placed, but confirmation email failed.")

        messages.success(request, "Your order has been placed!")
        return redirect('buyer:order_summary', order_id=order.id)

    return redirect('buyer:cart')

@buyer_required
def order_summary(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_confirmation.html', {'order': order})

@buyer_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_history.html', {'orders': orders})
