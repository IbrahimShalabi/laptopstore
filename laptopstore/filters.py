import django_filters
from.models import *

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        # fields ='__all__'
        fields = ['Laptop', 'status'] 
        exclude=['Coustomer']