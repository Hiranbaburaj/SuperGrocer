from django.urls import path
from . import views

urlpatterns = [
  path('supplier_dashboard/', views.supplier_dashboard, name='supplier_dashboard'),
  path('edit_supplier', views.edit_supplier, name='edit_supplier'),
  path('edit_supplierproduct/<int:supplierproduct_id>/', views.edit_supplierproduct, name='edit_supplierproduct'),
  path('delete_supplierproduct/<int:supplierproduct_id>/', views.delete_supplierproduct, name='delete_supplierproduct'),
  path('add_supplierproduct/', views.add_supplierproduct, name='add_supplierproduct'),

  path('purchase_orders_list/', views.purchase_orders_list, name='purchase_orders_list'),
  path('purchase_orders_approved/', views.purchase_orders_approved, name='purchase_orders_approved'),

  path('approve_purchaseorder/<int:purchase_order_id>/', views.approve_purchaseorder, name='approve_purchaseorder'),
  path('decline_purchaseorder/<int:purchase_order_id>/', views.decline_purchaseorder, name='decline_purchaseorder'),

]
