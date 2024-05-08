from django.db import models
from store.models import Product
from users.models import User

# Create your models here.

class Buyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link Buyer to User using OneToOneField
    buy_name = models.CharField(max_length=255,null=True)
    buy_address = models.TextField(null=True)
    buy_phone = models.CharField(max_length=20,null=True)
    buy_email = models.EmailField(unique=True)  # Ensure unique email for Buyers

    def __str__(self):
        return self.buy_name

class SalesOrder(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.SET_NULL, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)
    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_payment_signature = models.CharField(max_length=100, null=True, blank=True)    

    def __str__(self):
        return str(self.id)
        #return f"SalesOrder #{self.id} - Buyer: {self.buyer}, Date Ordered: {self.date_ordered}"

    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(SalesOrder, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
        #return f"OrderItem #{self.id} - Product: {self.product}, Quantity: {self.quantity}"

    @property
    def get_total(self):
        total = self.product.sell_price * self.quantity
        return total