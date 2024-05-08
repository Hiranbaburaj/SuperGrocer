from django.urls import path
from . import views

urlpatterns = [
  path('shop/', views.shop, name='shop'),
  path('cart/', views.cart, name='cart'),
  path('checkout/', views.checkout, name='checkout'),
  path('update_item/', views.updateItem, name='update_item'),
  path('process_order/', views.processOrder, name='process_order'),
  path('edit_buyer/', views.edit_buyer, name='edit_buyer'),
  path('update_inventory/', views.update_inventory, name='update_inventory'),
]