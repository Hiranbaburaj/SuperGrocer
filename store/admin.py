from django.contrib import admin

from store.models import Category, Inventory, Product, SubCategory

# Register your models here.
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)
admin.site.register(Inventory)