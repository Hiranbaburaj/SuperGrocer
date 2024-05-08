from django.urls import path
from . import views

urlpatterns = [
    path('product_list/', views.product_list, name='product_list'),
    path('add_product/', views.add_product, name='add_product'),
    path('edit_product/<str:prod_id>/', views.edit_product, name='edit_product'),
    path('delete_product/<str:prod_id>/', views.delete_product, name='delete_product'),
    path('product/<int:product_id>/', views.product_info, name='product_info'),

    path('category_list/', views.category_list, name='category_list'),
    path('add_category/', views.add_category, name='add_category'),
    path('delete_category/<str:cat_id>/', views.delete_category, name='delete_category'),
    path('subcategory_list/', views.subcategory_list, name='subcategory_list'),
    path('add_subcategory/', views.add_subcategory, name='add_subcategory'),
    path('delete_subcategory/<str:scat_id>/', views.delete_subcategory, name='delete_subcategory'),

    path('place_purchaseorder/', views.place_purchaseorder, name='place_purchaseorder'),  
    path('ajax/load-suppliers/', views.load_suppliers, name='ajax_load_suppliers'), # AJAX
    path('ajax/calculate_order_amount/', views.calculate_order_amount, name='ajax_calculate_order_amount'),
    path('purchaseorder_list/', views.purchaseorder_list, name='purchaseorder_list'),
    path('goods_received/<str:purchase_order_id>/', views.goods_received, name='goods_received'),

    path('purchases/', views.purchase_list, name='purchase_list'),
    path('inventory_list/', views.inventory_list, name='inventory_list'),
    
    path('sales_list/', views.sales_list, name='sales_list'),
    path('sales_info/<str:sales_order_id>/', views.sales_info, name='sales_info'),    
]