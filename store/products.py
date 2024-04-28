from supplier.models import SupplierProduct

def get_available_suppliers(product):
    """
    Fetches available suppliers for a given product, considering stock levels.
    """
    return SupplierProduct.objects.filter(prod_id=product, stock__gt=0).order_by('supply_price')
