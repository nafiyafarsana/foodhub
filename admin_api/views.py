from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


from user_api.authentication import JWTUserAuthentication
from vendor_api.models import Vendor
from .serializer import UpdateVendorSerializer,CategorySerializer,AddMenuFoodSerializer
from vendor_api.serializer import VendorSerializer
from user_api.serializers import UserSerializer,OrderSerializer
from user_api.models import User,Order
from .task import send_menumail_func
from .models import Menu

from django.core.mail import send_mail
# from django.template.defaultfilters import slugify

# Create your views here.


class VendorAllList(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTUserAuthentication]
    serializer_class = VendorSerializer
    
    def get(self, request):
        
        try:
            all_vendors = Vendor.objects.all()
            serializer = VendorSerializer(all_vendors,many=True)
            return Response(serializer.data)
        
        except:
                message = {'detail':'somthing whent worng'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)

class VendorDetailsView(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTUserAuthentication]
    serializer_class = VendorSerializer
    
    def get(self, request,id):
        try:
            vendor = Vendor.objects.get(id=id)
            serializer = VendorSerializer(vendor)
            return Response(serializer.data)
        
        except:
              message = {'message':'No Vendor with this id exist'}
              return Response(message)
              
    
class VerifyVendor(APIView):
    # permission_classes = [IsAdminUser]
    # authentication_class = [JWTUserAuthentication]
    # serializer_class = VendorSerializer     
    def get(self, request,id):
        
        try:
            details = Vendor.objects.get(id=id)
            details.is_active = True
            serializer = UpdateVendorSerializer(details,data=request.data,partial=True)
            print(serializer)
            if serializer.is_valid():
                serializer.save()

                
                email = details.email
                
                send_mail('Hello  ',
                  'Congratulations, your Vender application is approved.',
                  'nafiyafarsana944@gmail.com'
                  ,[email] ,  
                   fail_silently=False)
                
                print("VENDOR VERIFIED SUCCESSFULLY")
                return Response(serializer.data)
            
            else:
                print("VENDOR VERIFICATION FAILED")
                print(serializer.errors)
                return Response(serializer.errors)
            
        except:
            message = {'detail' : 'something went wrong'}
            return Response(message,status=status.HTTP_400_BAD_REQUEST)
        

class BlockVendor(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTUserAuthentication]
    
    def get(self,request,id):
        try:
            vendor = Vendor.objects.get(id=id)
            if vendor.is_active:
                vendor.is_active = False
            else:
                vendor.is_active = True
            serializer = UpdateVendorSerializer(vendor,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                print("Vendor Action Successfull")
                return Response(serializer.data)
            
            else:
                print('Vendor Action Failed')
                print(serializer.errors)
                return Response(serializer.errors)
            
                    
        except:
               message = {'detail' : 'something went wrong'}
               return Response(message,status=status.HTTP_400_BAD_REQUEST)
           

class UsersListView(APIView):
    permission_classes =  [IsAdminUser]
    authentication_classes = [JWTUserAuthentication]
    serializer_class = UserSerializer
    
    def get(self,request):
        try:
            all_users = User.objects.all()
            serializer = UserSerializer(all_users,many=True)
            return Response(serializer.data)
        
        except:
                message = {'detail':'somthing whent worng'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            

class UsersDetailsView(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTUserAuthentication]
    serializer_class = UserSerializer
    
    def get(self,request,id):
        try:
            user = User.objects.get(id=id)
            serializer = VendorSerializer(user)
            return Response(serializer.data)
        
        except:
              message = {'message':'No user with this id exist'}
              return Response(message)
        
        
class BlockUser(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTUserAuthentication]
    
    def get(self,request,id):
        try:
            user = User.objects.get(id=id)
            if user.is_active:
                user.is_active = False
            else:
                user.is_active = True
            serializer = UpdateVendorSerializer(user,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                print("user Action Successfull")
                return Response(serializer.data)
            
            else:
                print('user Action Failed')
                print(serializer.errors)
                return Response(serializer.errors)
            
                    
        except:
               message = {'detail' : 'something went wrong'}
               return Response(message,status=status.HTTP_400_BAD_REQUEST)
           
           
           
class AddcategoryView(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTUserAuthentication]
    
    def post(self,request,id):
        try:
            data = request.data
            request.data_mutable = True
            serializers= CategorySerializer(data=data)
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data)
            else:
                print(serializers.errors)
                return Response(serializers.errors)
            
        except:
            message = {'detail':'something went wrong'}
            return Response(message,status.HTTP_400_BAD_REQUEST)
        
class AddFoodView(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTUserAuthentication]
    
    def post(self,request):
        try:
            serializer = AddMenuFoodSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                print(serializer.data['food_name'])
                food_name = serializer.data['food_name']
                print(food_name)
                
                # send_menumail_func.delay()
                print('jcjnvjfvjfj')
                return Response(serializer.data)
            else:
                print(serializer.errors)
                return Response(serializer.errors)
            
        except Exception as e:
            raise e

class BlockFoodView(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTUserAuthentication]
    
    def patch(self,request,id):
        try:
            food_name = Menu.objects.get(id=id)
            if food_name.is_active == True:
                food_name.is_active = False
            else:
                food_name.is_active = True
            print(food_name.is_active)
            
            serializer = AddMenuFoodSerializer(food_name,data=request.data,partial = True)
            if serializer.is_valid():
                serializer.save()
                print("Your Action Successfull")
                return Response(serializer.data)
            else:
                print('Your Action Failed')
                print(serializer.errors)
                return Response(serializer.errors)
            
        except:
            message = {'detail':'something went wrong'}
            return Response(message,status.HTTP_400_BAD_REQUEST)
                
                
class UpdateFood(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTUserAuthentication]
    def patch(self,request,id):
        try:
            food_name = Menu.objects.get(id=id)
            serializer = AddMenuFoodSerializer(food_name,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                print("Food Updated Successfully")
                print(serializer.data)
                return Response(serializer.data)
            else:
                print("Food Updation failed")
                print(serializer.errors)
                return Response(serializer.errors)
        except Exception as e:
           raise e
        
    def delete(self,request,id):
        try:
            
            details = Menu.objects.get(id=id)
            details.delete()
            return Response({'message':'food is removed'})
        except Exception as e:
            raise e

        
class FoodDetails(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTUserAuthentication]
    def get(self,request):
        try:
            food_name = Menu.objects.all()
            serializer = AddMenuFoodSerializer(food_name,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                print(serializer.errors)
                return Response(serializer.errors)
        except Exception as e:
            raise e
        

        
class GetAllPaidOrders(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTUserAuthentication]
    serializer_class = VendorSerializer
    
    def get(self,request):
        try:
            orders = Order.objects.get(payment_status=True)
            serializer = OrderSerializer(orders,many=True)
            return Response(serializer.data)
        except Exception as e:
            raise e

        
       
        
            
                
                
                