from rest_framework import serializers
from . models import User,PaymentModel,Order,OrderItem




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

        extra_kwargs = {
            'password' : {'write_only' : True}
        }
        
    def validate_password(self,value):
        if len(value)<4:
            raise serializers.ValidationError("Password must be minimum 4 characters")
        else:
            return value
    def save(self):
        reg = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            phone_number=self.validated_data['phone_number'],
        )
        password=self.validated_data['password']
        reg.set_password(password)
        reg.save()
        return reg
    
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentModel
        fields = '__all__'

# class FoodChoices(object):
#     def __init__(self,choices,multiplechoices):
#         self.choices = choices
#         self.multiplechoices = multiplechoices
        

# # create a tuple

# FOOD_CHOICES = (
#     ("1","Vegetarian_Foods"),
#     ("2","Non_Vegetarian"),
#     ("3","Biriyani"),
#     ("4","Dosa"),
#     ("5","Beverages"),
#     ("6","Fast_Food"),
# )

# class FoodChoicesSerializer(serializers.Serializer):
#     # initialize fields
#     choices = serializers.ChoiceField(
#         choices= FOOD_CHOICES
#     )
#     multiplechoices = serializers.MultipleChoiceField(
#           choices = FOOD_CHOICES
#     )
    
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
        