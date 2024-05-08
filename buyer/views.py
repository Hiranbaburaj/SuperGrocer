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
import razorpay
from django.conf import settings
# Create your views here.

client = razorpay.Client(auth=(settings.KEY, settings.SECRET))

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
    order.transaction_id = transaction_id
    order.save()

    total = float(data['form']['total'])
    payment = client.order.create({
      'amount': total * 100,  # Convert to paise
      'currency': 'INR',
      'payment_capture': 1  # Capture payment automatically
    })

    # Response data includes payment details
    response_data = {
      'payment': {
        'amount': payment['amount'] / 100,  # Convert back to currency units
        'id': payment['id']
      }
    }

    if payment['status'] == 'created':  # Payment created successfully
      # **Inventory Update Logic:**
      update_inventory(order)  # Call your inventory update function

      # Order complete (modify as per your logic)
      order.complete = True
      order.razorpay_order_id = payment['id']
      order.save()

      return JsonResponse(response_data, safe=False)

    else:  # Payment creation failed
      return JsonResponse({'error': 'Payment creation failed'}, safe=False)

  else:
    return JsonResponse({'error': 'You must be logged in to place an order'}, safe=False)
  
def update_inventory(order):
  for order_item in order.orderitem_set.all():
    product = order_item.product
    available_inventories = Inventory.objects.filter(product=product).order_by('id')  # Get ordered inventory entries

    for available_inventory in available_inventories:
      # Reduce quantity from available inventory
      quantity_to_deduct = min(available_inventory.inv_qty, order_item.quantity)
      order_item.quantity -= quantity_to_deduct
      available_inventory.inv_qty -= quantity_to_deduct

      # Update or delete inventory
      if available_inventory.inv_qty > 0:
        available_inventory.save()
      else:
        available_inventory.delete()

      # Break loop if order item quantity is fulfilled
      if order_item.quantity == 0:
        break

    # Check if order item quantity was not fulfilled entirely
    if order_item.quantity > 0:
      raise Exception('Insufficient inventory for ' + str(order_item.product))  # Raise an exception or handle as needed

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
  
@login_required
def sale_list(request):
    buyer = request.user.buyer
    sales = buyer.salesorder_set.filter(complete=True).order_by('-id').order_by('-id') 
    context = {
        'sales': sales
    }
    return render(request, 'buyer/sale_list.html', context)

def sale_info(request, sales_order_id):
    order_items = OrderItem.objects.filter(order_id=sales_order_id)
    return render(request, 'store/sale_info.html', {'order_items': order_items})