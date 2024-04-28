from django.db import models

# Create your models here.

class Category(models.Model):
    cat_name = models.CharField(max_length=100)

    def __str__(self):
        return self.cat_name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    scat_name = models.CharField(max_length=100)

    def __str__(self):
        return self.scat_name

class Product(models.Model):
    prod_name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    sell_price = models.DecimalField(max_digits=10, decimal_places=2)
    prod_desc = models.TextField()
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.prod_name

class Inventory(models.Model):
    purchase_id = models.CharField(max_length=20)   #purchase ID
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    inv_qty = models.PositiveIntegerField()
    exp_date = models.DateField(null=True, blank=True)
    sell_price = models.DecimalField(max_digits=10, decimal_places=2)  # DecimalField for sell price

    def __str__(self):
        return f"Inventory {self.id}"

