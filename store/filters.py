from django import forms
from django_filters import FilterSet, CharFilter, ModelChoiceFilter
from .models import Product, Category, SubCategory

class ProductFilter(FilterSet):
    prod_name = CharFilter(lookup_expr='icontains', 
                           label='Product Name',
                           widget=forms.TextInput(attrs={'class': 'form-control'}))  # Case-insensitive search
    
    category = ModelChoiceFilter(queryset=Category.objects.all(), label='Category',
                                 widget=forms.Select(attrs={'class': 'form-select'}))
    subcategory = ModelChoiceFilter(queryset=SubCategory.objects.all(), label='Subcategory',
                                    widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Product
        fields = ['prod_name', 'category', 'subcategory']


