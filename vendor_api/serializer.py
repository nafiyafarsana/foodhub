from rest_framework import serializers
from .models import Vendor,RestMenuModel,RestFoodModel,AddTime
from django.contrib.auth.hashers import make_password



class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ["id",'vendor_name','email',"phone_number","password","license"]  

        extra_kwargs = {
            'password' : {'write_only' : True}
        }
    
    def validate_password(self,value):
        if len(value)<4:
            raise serializers.ValidationError("Password must be minimum 4 charecters")
        else:
            return value
    def validate_phone_number(self,value):
        if len(value)!=10:
            raise serializers.ValidationError("Phonenumber must be minimum 10 digits")
        else:
            return value
    def save(self):
        reg = Vendor.objects.create(
            email=self.validated_data['email'],
            phone_number=self.validated_data['phone_number'],
            # password=self.validated_data['password'], 
            password = make_password(self.validated_data['password']),
        )
        print(reg)
        
        return reg
    
class RestMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestMenuModel
        fields = '__all__'
        
class RestFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestFoodModel
        fields = '__all__'
        

class AddRestTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddTime
        fields = '__all__'