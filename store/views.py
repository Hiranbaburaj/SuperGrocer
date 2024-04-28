from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect

from supplier.models import PurchaseOrder, SupplierProduct, Purchase
from .models import Category, SubCategory, Product, Inventory
from .forms import CategoryForm, PurchaseOrderForm, SubCategoryForm, ProductForm

from pyexpat.errors import messages
from django.contrib.messages import success

from buyer.models import SalesOrder, OrderItem

# Create your views here.

from .filters import ProductFilter

def product_list(request):
    products = Product.objects.all()
    product_filter = ProductFilter(request.GET, queryset=products)  # Apply filters
    products = product_filter.qs

    context = {'products': products, 'product_filter': product_filter}  # Pass filter to template
    return render(request, 'store/product_list.html', context)

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list') 
    else:
        form = ProductForm()
    return render(request, 'store/add_product.html', {'form': form})

def edit_product(request, prod_id):
    product = get_object_or_404(Product, id=prod_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # Redirect to the product list page
    else:
        form = ProductForm(instance=product)
    return render(request, 'store/edit_product.html', {'form': form, 'product': product})

def delete_product(request, prod_id):
    product = get_object_or_404(Product, id=prod_id)
    if request.method == 'POST':
        # Confirm deletion
        product.delete()
        return redirect('product_list')  # Redirect to the product list page
    return render(request, 'store/delete_product.html', {'product': product})

def product_info(request, product_id):
  """
  This view retrieves and displays details of a product based on its ID.
  """
  product = get_object_or_404(Product, pk=product_id)
  context = {'product': product}
  return render(request, 'product_info.html', context)

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'store/category_list.html', {'categories': categories})

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list') 
    else:
        form = CategoryForm()
    return render(request, 'store/add_category.html', {'form': form})

def delete_category(request, cat_id):
    category = get_object_or_404(Category, id=cat_id)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'store/delete_category.html', {'category': category})

def subcategory_list(request):
    subcategories = SubCategory.objects.all()
    return render(request, 'store/subcategory_list.html', {'subcategories': subcategories})

def add_subcategory(request):
    if request.method == 'POST':
        form = SubCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subcategory_list') 
    else:
        form = SubCategoryForm()
    return render(request, 'store/add_subcategory.html', {'form': form})

def delete_subcategory(request, scat_id):
    subcategory = get_object_or_404(SubCategory, id=scat_id)
    if request.method == 'POST':
        subcategory.delete()
        return redirect('subcategory_list')
    return render(request, 'store/delete_subcategory.html', {'subcategory': subcategory})


def place_purchaseorder(request):
    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            supplier_product = get_object_or_404(SupplierProduct, product=order.product, supplier=order.supplier)

            if order.ord_qty > supplier_product.stock:
                return JsonResponse({'error': 'Quantity exceeds available stock.'})

            order.ord_amount = order.ord_qty * supplier_product.supply_price
            order.save()

            # Deduct the order quantity from the stock
            supplier_product.stock -= order.ord_qty
            supplier_product.save()

            return redirect('purchaseorder_list')
        else:
            return JsonResponse({'error': 'Invalid form data.'})
    else:
        form = PurchaseOrderForm()
        return render(request, 'store/place_purchaseorder.html', {'form': form})

def load_suppliers(request):
    product_id = request.GET.get('product_id')
    print(f"The PRODUCT ID: {product_id}")
    if product_id:
        suppliers = SupplierProduct.objects.filter(product=product_id, availability=True).order_by('supplier__spl_name') 
        return render(request, 'store/supplier_dropdown_list_options.html', {'suppliers': suppliers})
    else:
        return JsonResponse([], safe=False)  # Return an empty list if no product ID is provided
   
def calculate_order_amount(request):
    if request.method == 'GET' and all(param in request.GET for param in ['product_id', 'supplier_id', 'quantity']):
        product_id = int(request.GET['product_id'])
        supplier_id = int(request.GET['supplier_id'])
        quantity = int(request.GET['quantity'])

        supplier_product = get_object_or_404(SupplierProduct, product_id=product_id, supplier_id=supplier_id)
        if quantity > supplier_product.stock:
            return JsonResponse({'error': 'Quantity exceeds available stock.'})

        ord_amount = quantity * supplier_product.supply_price
        return JsonResponse({'ord_amount': ord_amount})
    else:
        return JsonResponse({'error': 'Invalid request'})

def purchaseorder_list(request):
  purchase_orders = PurchaseOrder.objects.all()
  context = {'purchase_orders': purchase_orders}
  return render(request, 'store/purchaseorder_list.html', context)

def goods_received(request, purchase_order_id):
  try:
    purchase_order = PurchaseOrder.objects.get(pk=purchase_order_id)
    if purchase_order.status == 'approved':
      # Create Purchase record
      purchase = Purchase.objects.create(
          order=purchase_order,
          supplier=purchase_order.supplier,
          product=purchase_order.product,
          ord_qty=purchase_order.ord_qty,
      )
      # Update PurchaseOrder status
      purchase_order.status = 'complete'
      purchase_order.save()

      # Create Inventory record
      inventory = Inventory.objects.create(
          purchase_id=purchase.id,  # Use Purchase object ID
          product=purchase_order.product,
          inv_qty=purchase_order.ord_qty,
          sell_price=purchase_order.product.sell_price,  # Assuming sell_price is in PurchaseOrder
      )
      # Success message (optional)
      success(request, 'Goods received successfully!')
  except PurchaseOrder.DoesNotExist:
    messages.error(request, 'Purchase Order not found!')
  return redirect('purchaseorder_list')  # Redirect to purchase order list


def inventory_list(request):
  inventories = Inventory.objects.all()  # Fetch all inventory items
  context = {'inventories': inventories}
  return render(request, 'store/inventory_list.html', context)


def sales_list(request):
    sales_orders = SalesOrder.objects.filter(complete=True).order_by('-date_ordered')
    return render(request, 'store/sales_list.html', {'sales_orders': sales_orders})


def sales_info(request, sales_order_id):
    order_items = OrderItem.objects.filter(order_id=sales_order_id)
    return render(request, 'store/sales_info.html', {'order_items': order_items})

def purchase_list(request):
  """
  This view retrieves and displays a list of all purchases from the Purchase model.
  """
  purchases = Purchase.objects.all().order_by('-p_date').select_related('order', 'supplier', 'product')  # Optimize query
  context = {'purchases': purchases}
  return render(request, 'store/purchase_list.html', context)