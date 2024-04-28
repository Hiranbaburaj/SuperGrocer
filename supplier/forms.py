from django import forms
from .models import Supplier, SupplierProduct

class EditSupplierProductForm(forms.ModelForm):
    class Meta:
        model = SupplierProduct
        fields = ['supply_price', 'stock', 'availability']
        labels = {
            'supply_price': 'Supply Price',
            'stock': 'Stock',
            'availability': 'Availability',
        }
        widgets = {
            'supply_price': forms.TextInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'availability': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class AddSupplierProductForm(forms.ModelForm):
    class Meta:
        model = SupplierProduct
        fields = ['product', 'stock', 'availability']  # Remove 'supply_price' from fields
        labels = {
            'product': 'Product',
            'stock': 'Stock',
            'availability': 'Availability',
        }
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'availability': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        self.supplier = kwargs.pop('supplier', None)  # Get the 'supplier' argument
        super().__init__(*args, **kwargs)  # Call the parent constructor
        # Set the initial supply_price based on the selected product's sell_price
        if 'instance' in kwargs and kwargs['instance'] is not None:
            self.fields['supply_price'].initial = kwargs['instance'].product.cost_price

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['supplier'] = self.supplier  # Access supplier from kwargs
        return cleaned_data
    
class EditSupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['spl_name', 'spl_address', 'spl_phone']
        labels = {
            'spl_name': 'Supplier Name',
            'spl_address': 'Supplier Address',
            'spl_phone': 'Supplier Phone Number',
        }
        widgets = {
            'spl_name': forms.TextInput(attrs={'class': 'form-control'}),
            'spl_address': forms.Textarea(attrs={'class': 'form-control'}),
            'spl_phone': forms.TextInput(attrs={'class': 'form-control'}),
        }
