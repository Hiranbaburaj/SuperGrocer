from django import forms

from supplier.models import PurchaseOrder, Supplier, SupplierProduct
from .models import Product, Category, SubCategory

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['prod_name', 'category', 'subcategory', 'cost_price', 'sell_price', 'prod_desc', 'image']
        labels = {
            'prod_name': 'Product Name',
            'category': 'Category',
            'subcategory': 'Subcategory',
            'cost_price': 'Cost Price',
            'sell_price': 'Sell Price',
            'prod_desc': 'Description',
            'image': 'Product Image',  # Add label for image field
        }
        widgets = {
            'prod_name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'subcategory': forms.Select(attrs={'class': 'form-select'}),
            'cost_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'sell_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'prod_desc': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),  # Use FileInput widget
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['cat_name']
        labels = {
            'cat_name': 'Category Name',
        }
        widgets = {
            'cat_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['category', 'scat_name']
        labels = {
            'category': 'Category',
            'scat_name': 'Subcategory Name',
        }
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'scat_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['product', 'supplier', 'ord_qty', 'ord_amount'] 
        labels = {
            'product': 'Product',
            'supplier': 'Supplier',
            'ord_qty': 'Quantity',
            'ord_amount': 'Total Amount',
        }
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'ord_qty': forms.NumberInput(attrs={'class': 'form-control'}),
            'ord_amount': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),  # Read-only
        }

    def clean_ord_qty(self):
        ord_qty = self.cleaned_data.get('ord_qty')
        product = self.cleaned_data.get('product')
        if product:
            supplier_product = SupplierProduct.objects.filter(product=product, availability=True).first()
            if supplier_product and ord_qty > supplier_product.stock:
                raise forms.ValidationError("Quantity exceeds available stock.")
        return ord_qty