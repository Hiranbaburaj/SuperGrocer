from datetime import timezone
from django.db import models
from users.models import User
from store.models import Product

# Create your models here.

class Supplier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link Supplier to User using OneToOneField
    spl_name = models.CharField(max_length=255,null=True)
    spl_address = models.TextField(null=True)
    spl_phone = models.CharField(max_length=20,null=True)
    spl_email = models.EmailField(unique=True)  # Ensure unique email for suppliers

    def __str__(self):
        return self.spl_name
    
class SupplierProduct(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    supply_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.supplier} - {self.product.prod_name}"
    
class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('decline', 'Decline'),
        ('approved', 'Approved'),
        ('processing', 'Processing'),
        ('complete', 'Complete'),
    ]

    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    ord_date = models.DateField(auto_now_add=True)
    ord_amount = models.DecimalField(max_digits=10, decimal_places=2)
    ord_qty = models.PositiveIntegerField()

    def __str__(self):
        return f"Order {self.id} - {self.status}"

class Purchase(models.Model):
    order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    p_date = models.DateField(auto_now_add=True)
    ord_qty = models.PositiveIntegerField()

    def __str__(self):
        return f"Purchase {self.id}"