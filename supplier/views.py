from pyexpat.errors import messages
from django.contrib.messages import success
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import PurchaseOrder, SupplierProduct, Product
from .forms import AddSupplierProductForm, EditSupplierForm, EditSupplierProductForm

@login_required
def supplier_dashboard(request):
    supplier = request.user.supplier  # Access the logged-in supplier's details
    supplier_products = SupplierProduct.objects.filter(supplier=supplier)
    context = {'supplier_products': supplier_products}
    return render(request, 'supplier/supplier_dashboard.html', context)

def edit_supplierproduct(request, supplierproduct_id):  
    supplier_product = get_object_or_404(SupplierProduct, pk=supplierproduct_id)

    if request.method == 'POST':
        form = EditSupplierProductForm(request.POST, instance=supplier_product)
        if form.is_valid():
            form.save()
            return redirect('supplier_dashboard')
    else:
        form = EditSupplierProductForm(instance=supplier_product)

    context = {'form': form, 'supplier_product': supplier_product}
    return render(request, 'supplier/edit_supplierproduct.html', context)

@login_required
def delete_supplierproduct(request, supplierproduct_id):
    supplier_product = get_object_or_404(SupplierProduct, pk=supplierproduct_id)
    supplier_product.delete()
    return redirect('supplier_dashboard')

@login_required
def add_supplierproduct(request):
    supplier = request.user.supplier
    products = Product.objects.all()
    if request.method == 'POST':
        form = AddSupplierProductForm(request.POST, supplier=supplier)  # Pass supplier here
        if form.is_valid():
            form.instance.supplier = supplier  # Set supplier on form instance
            form.instance.supply_price = form.cleaned_data['product'].cost_price  # Set supply_price from sell_price
            form.save()
            return redirect('supplier_dashboard')
    else:
        form = AddSupplierProductForm(supplier=supplier)  # Pass supplier here

    context = {'form': form, 'products': products, 'supplier': supplier}
    return render(request, 'supplier/add_supplierproduct.html', context)

@login_required
def purchase_orders_list(request):
  supplier = request.user.supplier
  purchase_orders = PurchaseOrder.objects.filter(supplier=supplier, status='pending')  # Filter by pending status
  context = {'purchase_orders': purchase_orders}
  return render(request, 'supplier/purchase_orders_list.html', context)

@login_required
def purchase_orders_approved(request):
  supplier = request.user.supplier
  purchase_orders = PurchaseOrder.objects.filter(supplier=supplier, status='approved')  # Filter by pending status
  context = {'purchase_orders': purchase_orders}
  return render(request, 'supplier/purchase_orders_approved.html', context)


@login_required
def approve_purchaseorder(request, purchase_order_id):
  try:
    purchase_order = PurchaseOrder.objects.get(pk=purchase_order_id)
    if purchase_order.status == 'pending':
      purchase_order.status = 'approved'
      purchase_order.save()
      success(request, 'Purchase Order approved successfully!')  # Use success function
  except PurchaseOrder.DoesNotExist:
    messages.error(request, 'Purchase Order not found!')
  return redirect('purchase_orders_approved')


@login_required
def decline_purchaseorder(request, purchase_order_id):
  try:
    purchase_order = PurchaseOrder.objects.get(pk=purchase_order_id)
    if purchase_order.status == 'pending':
      purchase_order.status = 'decline'
      purchase_order.save()
      # Success message (optional)
      success(request, 'Purchase Order declined successfully!')
  except PurchaseOrder.DoesNotExist:
    # Error message if purchase order not found (optional)
    messages.error(request, 'Purchase Order not found!')
  return redirect('purchase_orders_list')  # Redirect to purchase order list view

@login_required
def edit_supplier(request):
    supplier = request.user.supplier  # Get the logged-in user's supplier

    if request.method == 'POST':
        form = EditSupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('edit_supplier')  # Redirect to supplier details page
    else:
        # Initial form with current supplier data
        form = EditSupplierForm(instance=supplier)

    context = {'form': form}
    return render(request, 'supplier/edit_supplier.html', context)