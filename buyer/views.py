import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from buyer.filters import ProductFilter

from .forms import EditBuyerForm
from store.models import Inventory
from .models import *
import datetime
from django.utils import timezone
from django.db import transaction
from django.db.models import Sum  # Import for quantity summation
# Create your views here.

@login_required
def shop(request):
  buyer = request.user.buyer
  order, created = SalesOrder.objects.get_or_create(buyer=buyer, complete=False)
  items = order.orderitem_set.all()
  cartItems = order.get_cart_items

  products = Product.objects.filter(
      pk__in=Inventory.objects.filter(inv_qty__gt=0).values_list('product', flat=True)
  )

  product_filter = ProductFilter(request.GET, queryset=products)  # Apply filters
  products = product_filter.qs
  context = {'products': products, 'cartItems': cartItems, 'product_filter': product_filter}
  return render(request, 'buyer/shop.html', context)

@login_required
def cart(request):
    if request.user.is_authenticated:
        buyer = request.user.buyer
        order, created = SalesOrder.objects.get_or_create(buyer=buyer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        items=[]
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'buyer/cart.html', context)    

@login_required
def checkout(request):
    if request.user.is_authenticated:
        buyer = request.user.buyer
        order, created = SalesOrder.objects.get_or_create(buyer=buyer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items=[]
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'buyer/checkout.html', context)    

@login_required
def updateItem(request):
    data = json.loads(request.body)
    ProductId = data['productId']
    action = data['Action']

    print(f"Action: {action}")
    print(f"ProductId: {ProductId}")

    buyer = request.user.buyer
    product = Product.objects.get(id=ProductId)
    order, created = SalesOrder.objects.get_or_create(buyer=buyer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    # Check available inventory using aggregation
    available_inventory = Inventory.objects.filter(product=product).aggregate(total_qty=Sum('inv_qty'))['total_qty'] or 0

    if action == 'add' and orderItem.quantity < available_inventory:
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item quantity updated', safe=False)

@login_required
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        buyer = request.user.buyer
        order, created = SalesOrder.objects.get_or_create(buyer=buyer, complete=False)
        order.date_ordered = timezone.now()
        order.save()

        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        cartItems = order.get_cart_items

        if cartItems == 0:
            return JsonResponse({'error': 'Cart is Empty'}, safe=False)

        else:
        # Validate order total (optional)
            if order.get_cart_total != total:
                return JsonResponse({'error': 'Order total mismatch'}, safe=False)

            with transaction.atomic():  # Wrap updates in an atomic transaction
                order.complete = True
                order.save()

                # Update inventory quantities for each order item
                for order_item in order.orderitem_set.all():
                    product = order_item.product
                    available_inventory = Inventory.objects.filter(product=product).first()  # Get first matching entry

                    # Check for sufficient inventory before update (optional)
                    if available_inventory and available_inventory.inv_qty < order_item.quantity:
                        return JsonResponse({'error': 'Insufficient inventory'}, safe=False)

                    if available_inventory:
                        available_inventory.inv_qty -= order_item.quantity
                        if available_inventory.inv_qty <= 0:  # Delete if quantity reaches 0
                            available_inventory.delete()
                        else:
                            available_inventory.save()

            return JsonResponse('Payment Complete', safe=False)
    else:
        return JsonResponse({'error': 'You must be logged in to place an order'}, safe=False)

@login_required
def edit_buyer(request):
    buyer = request.user.buyer  # Get the logged-in user's buyer

    if request.method == 'POST':
        form = EditBuyerForm(request.POST, instance=buyer)
        if form.is_valid():
            form.save()
            return redirect('shop')  # Redirect to buyer details page
    else:
        # Initial form with current buyer data
        form = EditBuyerForm(instance=buyer)

    context = {'form': form}
    return render(request, 'buyer/edit_buyer.html', context)
  