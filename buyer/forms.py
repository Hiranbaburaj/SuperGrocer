from django import forms

from .models import Buyer

class EditBuyerForm(forms.ModelForm):
    class Meta:
        model = Buyer
        fields = ['buy_name', 'buy_address', 'buy_phone']
        labels = {
            'buy_name': 'Buyer Name',
            'buy_address': 'Buyer Address',
            'buy_phone': 'Buyer Phone Number',
        }
        widgets = {
            'buy_name': forms.TextInput(attrs={'class': 'form-control'}),
            'buy_address': forms.Textarea(attrs={'class': 'form-control'}),
            'buy_phone': forms.TextInput(attrs={'class': 'form-control'}),
        }