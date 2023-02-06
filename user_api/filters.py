from django_filters.rest_framework import FilterSet
from vendor_api.models import RestFoodModel

class ItemFilterByPrice(FilterSet):
    class Meta:
        model = RestFoodModel
        fields = {
            'food_price' : ['gt' , 'lt'], 
        }