from rest_framework import serializers
from vendor_api.models import Vendor
from .models import Category,Menu
from user_api.models import User



class UpdateVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'
        extra_kwargs = {
            'password' : {'write_only' : True}
         }

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password' : {'write_only' : True}
        }
        
class AddMenuFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'