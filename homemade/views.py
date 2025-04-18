
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import HomeMadeItem
from .forms import HomeMadeItemForm
from buyer.models import OrderItem
@login_required(login_url='homemade:homemadelogin')
def homemade_home(request):
    if not request.user.is_homemade:
        return redirect('homemade:login')

    homemade_items = HomeMadeItem.objects.filter(homemade_user=request.user)
    form = HomeMadeItemForm()

    update_item = None
    if 'edit' in request.GET:
        update_item = get_object_or_404(HomeMadeItem, pk=request.GET['edit'], homemade_user=request.user)
        form = HomeMadeItemForm(instance=update_item)

    if request.method == 'POST':
        if 'reset' in request.POST:
            item_id = request.POST.get('reset')
            reset_item = get_object_or_404(HomeMadeItem, pk=item_id, homemade_user=request.user)
            reset_item.order_count = 0
            reset_item.save()
            return redirect('homemade:homemade_home')

        if update_item:
            form = HomeMadeItemForm(request.POST, request.FILES, instance=update_item)
        else:
            form = HomeMadeItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.homemade_user = request.user
            item.save()
            return redirect('homemade:homemade_home')

    return render(request, 'homemade_home.html', {
        'homemade_items': homemade_items,
        'form': form,
        'update_item': update_item
    })

# @login_required(login_url='homemade:homemadelogin')
# def homemade_home(request):
#     if not request.user.is_homemade:
#         return redirect('homemade:login')

#     homemade_items = HomeMadeItem.objects.filter(homemade_user=request.user)
#     form = HomeMadeItemForm()

#     if request.method == 'POST':
#         form = HomeMadeItemForm(request.POST, request.FILES)
#         if form.is_valid():
#             item_name = form.cleaned_data['item']
#             price = form.cleaned_data['price']
#             address = form.cleaned_data['address']
#             image = form.cleaned_data.get('image')

#             existing_item = HomeMadeItem.objects.filter(
#                 homemade_user=request.user, item=item_name
#             ).first()

#             if existing_item:
#                 existing_item.price = price
#                 existing_item.address = address
#                 if image:
#                     existing_item.image = image
#                 existing_item.save()
#             else:
#                 item = form.save(commit=False)
#                 item.homemade_user = request.user
#                 item.save()

#             return redirect('homemade:homemade_home')  # ✅ fixed

#     return render(request, 'homemade_home.html', {
#         'homemade_items': homemade_items,
#         'form': form,
#     })

@login_required(login_url='homemade:homemadelogin')
def delete_homemade_item(request, pk):
    if not request.user.is_homemade:
        return redirect('homemade:login')

    item = get_object_or_404(HomeMadeItem, pk=pk, homemade_user=request.user)
    item.delete()
    return redirect('homemade:homemade_home')  # ✅ fixed

@login_required(login_url='homemade:login')
def order_requests(request):
    if not request.user.is_homemade:
        return redirect('homemade:login')

    order_items = OrderItem.objects.filter(
        item__homemade_user=request.user
    ).select_related('order', 'item')

    return render(request, 'homemade_order_requests.html', {
        'order_items': order_items
    })
