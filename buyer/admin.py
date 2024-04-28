from django.contrib import admin

from buyer.models import Buyer, OrderItem, SalesOrder

# Register your models here.
admin.site.register(Buyer)
admin.site.register(SalesOrder)
admin.site.register(OrderItem)