from django import forms
from django_filters import FilterSet, CharFilter, ModelChoiceFilter
from store.models import Product

class ProductFilter(FilterSet):
    prod_name = CharFilter(lookup_expr='icontains', label='',  # Hide label
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search by product name'}))

    class Meta:
        model = Product
        fields = ['prod_name']