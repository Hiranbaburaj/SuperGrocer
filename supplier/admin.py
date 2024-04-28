from django.contrib import admin
from .models import Supplier, PurchaseOrder, Purchase, SupplierProduct

# Register your models here.
admin.site.register(Supplier)
admin.site.register(PurchaseOrder)
admin.site.register(Purchase)
admin.site.register(SupplierProduct)