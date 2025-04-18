# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from .forms import SellerItemForm
# from .models import SellerItem, DealItem, LocalItem  # Import LocalItem
# from .decorators import seller_required

# @seller_required
# def seller_home(request):
#     form = SellerItemForm()
#     seller_items = SellerItem.objects.filter(seller=request.user)
#     local_items = LocalItem.objects.filter(seller=request.user) # Fetch LocalItem for display
#     deal_items = DealItem.objects.filter(seller_item__seller=request.user)
#     update_item = None

#     if 'update' in request.GET:
#         item_id = request.GET['update']
#         update_item = get_object_or_404(LocalItem, id=item_id, seller=request.user)
#         form = SellerItemForm(instance=update_item)

#     if request.method == 'POST':
#         if 'add_deal' in request.POST:
#             seller_item_id = request.POST.get('seller_item_id')
#             deal_price = request.POST.get('deal_price')

#             if seller_item_id and deal_price:
#                 seller_item = get_object_or_404(SellerItem, id=seller_item_id, seller=request.user)
#                 DealItem.objects.create(seller_item=seller_item, deal_price=deal_price)
#                 return redirect('seller:seller_home')
#         else: # Handle the "Add/Update Item" form submission
#             item_id = request.POST.get('item_id')
#             if item_id:
#                 # Update existing item (using LocalItem)
#                 local_item = get_object_or_404(LocalItem, id=item_id, seller=request.user)
#                 form = SellerItemForm(request.POST, instance=local_item)
#             else:
#                 # Add new item
#                 form = SellerItemForm(request.POST)

#             if form.is_valid():
#                 # We need to create a SellerItem first to trigger the save method
#                 seller_item = SellerItem(seller=request.user, **form.cleaned_data)
#                 seller_item.save() # This will create/update LocalItem as well
#                 return redirect('seller:seller_home')

#     context = {
#         'form': form,
#         'seller_items': seller_items,
#         'local_items': local_items, # Pass LocalItem to the template
#         'deal_items': deal_items,
#         'update_item': update_item,
#         'update_mode': update_item is not None,
#     }
#     return render(request, 'seller_home.html', context)

# @seller_required
# def delete_item(request, pk):
#     item = get_object_or_404(SellerItem, id=pk, seller=request.user)
#     item.delete()
#     return redirect('seller:seller_home')

# @seller_required
# def delete_deal_item(request, pk):
#     deal_item = get_object_or_404(DealItem, id=pk, seller_item__seller=request.user)
#     deal_item.delete()
#     return redirect('seller:seller_home')

# @seller_required
# def main_home(request):
#     return render(request, 'main_home.html')



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import SellerItemForm
from .models import SellerItem, DealItem, LocalItem
from .decorators import seller_required

@seller_required
def seller_home(request):
    form = SellerItemForm()
    seller_items = SellerItem.objects.filter(seller=request.user)
    local_items = LocalItem.objects.filter(seller=request.user)
    deal_items = DealItem.objects.filter(seller_item__seller=request.user)
    update_item = None

    if 'update' in request.GET:
        item_id = request.GET['update']
        update_item = get_object_or_404(LocalItem, id=item_id, seller=request.user)
        form = SellerItemForm(instance=update_item)

    if request.method == 'POST':
        if 'add_deal' in request.POST:
            seller_item_id = request.POST.get('seller_item_id')
            deal_price = request.POST.get('deal_price')

            if seller_item_id and deal_price:
                seller_item = get_object_or_404(SellerItem, id=seller_item_id, seller=request.user)
                DealItem.objects.create(seller_item=seller_item, deal_price=deal_price)
                return redirect('seller:seller_home')
        else:
            item_id = request.POST.get('item_id')
            if item_id:
                local_item = get_object_or_404(LocalItem, id=item_id, seller=request.user)
                form = SellerItemForm(request.POST, request.FILES, instance=local_item)
            else:
                form = SellerItemForm(request.POST, request.FILES)

            if form.is_valid():
                seller_item = SellerItem(seller=request.user, **form.cleaned_data)
                seller_item.save()
                return redirect('seller:seller_home')

    context = {
        'form': form,
        'seller_items': seller_items,
        'local_items': local_items,
        'deal_items': deal_items,
        'update_item': update_item,
        'update_mode': update_item is not None,
    }
    return render(request, 'seller_home.html', context)

@seller_required
def delete_item(request, pk):
    item = get_object_or_404(SellerItem, id=pk, seller=request.user)
    item.delete()
    return redirect('seller:seller_home')

@seller_required
def delete_deal_item(request, pk):
    deal_item = get_object_or_404(DealItem, id=pk, seller_item__seller=request.user)
    deal_item.delete()
    return redirect('seller:seller_home')

@seller_required
def main_home(request):
    return render(request, 'main_home.html')







