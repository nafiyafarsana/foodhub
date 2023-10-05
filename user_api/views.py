import requests
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination

from . models import User,UserToken,Order,OrderItem
from . serializers import UserSerializer,PaymentSerializer,OrderSerializer,OrderItemSerializer
from .verify import check,send

from admin_api.models import Category
from admin_api.serializer import CategorySerializer,UpdateUserSerializer

from vendor_api.models import RestFoodModel
from vendor_api.serializer import RestFoodSerializer
from vendor_api.myauth import TokenAuthenticationSafe

import datetime
from .authentication import JWTUserAuthentication,create_access_token,create_refresh_token

from twilio.rest import Client
import random
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend

import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.utils.datastructures import MultiValueDictKeyError
from django.db.models import Q
from .custom import *

from .filters import ItemFilterByPrice


# Create your views here.

class UserRegister(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    
    def post(self,request):
        data = request.data
        serializer = self.serializer_class(data=data)
        
        
        if serializer.is_valid():
            serializer.save()
            
            response = {
                "messages" : "User created successfully",
                "data" : serializer.data
            }
            
            return Response (data=response,status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class UserLogin(APIView):
    def post(self,request):
        try:
            phone_number = request.data['phone_number']
            print('1')
            password = request.data['password']
            print('1')

            user = User.objects.get(phone_number=phone_number)
            print(user)
            if user is None:
                response = Response()
            
                response.data={
                    'message':'Invalid phone_number'
                }
                return response
                print('3')

            if not user.check_password(password):
                response = Response()
            
                response.data={
                    'message':'invalid password'
                }
                return response

           
            if user:
                
                access_token = create_access_token(user.id)
                refresh_token = create_refresh_token(user.id)
                UserToken.objects.create(
                    user_id=user.id,
                    token=refresh_token,
                    expired_at=datetime.datetime.utcnow() + datetime.timedelta(days=7)
                )

                response = Response()
                
                response.set_cookie(key='refresh_token',value=refresh_token,httponly=True)
                response.data = {
                    'token': access_token,
                    'admin': user.is_admin,
                    
                }
                return response
            else:
                response = Response()
                response.data={
                    'message':'Not verified'
                }
                return response  
        except:
            message = {'detail':'somthing went wrong'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


class LoginUserWithOtpAPIView(APIView):
    def post(self, request):
        """ required field : phone_number-10 digit number """
    
        phone_number = request.data['phone_number']

        user = User.objects.filter(phone_number=phone_number,is_active=True)
        print(user)
        if user is None:
            response = Response()
            print(user)
            response.data={
                'message':'Invalid phone_number'
            }
            return response

        if user:
            print('otp sented....')
            print(user)
            print(phone_number)
            send(phone_number)
            response = Response()
            response.set_cookie(key='phone_number',value=phone_number,httponly=True)
            response.data = {
            'phone_number':phone_number
            }
            return response
        else:
            response = Response()
            response.data={
                'message':'No user in this phone number'
            }
            return response 
     

class VerifyLoginUserOtp(APIView):
    def post(self,request):

        """ required field : code - string"""
        try:
            data=request.data
            phone_number=request.COOKIES.get('phone_number')
            code=data['code']
            if check(phone_number,code):
                user = User.objects.filter(phone_number=phone_number).first()
                print(user)
                if user:
                   
                    # response.delete_cookie(key='phone_number')
                    access_token = create_access_token(user.id)
                    refresh_token = create_refresh_token(user.id)
                    UserToken.objects.create(
                        user_id=user.id,
                        token=refresh_token,
                        expired_at=datetime.datetime.utcnow() + datetime.timedelta(days=7)
                    )

                    response = Response()
                    
                    response.set_cookie(key='refresh_token',value=refresh_token,httponly=True)
                    response.data = {
                        'token': access_token,
                        'admin': user.is_admin,
                        
                    }
                    return response
                else:
                    response = Response()
                    response.data={
                        'message':'Not verified'
                    }
                    return response 
            else:
                message = {'detail':'otp is not valid'}
                
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
        except:
            message = {'detail':'somthing went wrong'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
        

class UserAPIView(APIView):
    authentication_classes = [JWTUserAuthentication]
    def get(self,request):
        try:
            return Response(UserSerializer(request.user).data)
        except:
            message = {'detail':'somthing went wrong'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        

class UserLogoutApiView(APIView):
    def post(self,request):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            print(refresh_token)
            UserToken.objects.filter(token=refresh_token).delete()
            response = Response()
            
            try:
                response.delete_cookie(key='refresh_token')
                response.delete_cookie(key='phone_number')
            except:
                response.delete_cookie(key='refresh_token')
            response.data = {
                 'message' : 'User Logged out successfully'
            }
            return response
        except:
            message = {'detail':'something went wrong'}
            return Response(message,status=status.HTTP_400_BAD_REQUEST)
        

class AllCategories(APIView):
    # permission_classes = [JWTUserAuthentication]
    def get(self,request):
        try:
            user = request.data
            category = Category.objects.all()
            serializer = CategorySerializer(category,many=True)
            return Response(serializer.data)
        except:
            message = {'detail' : 'something went wrong'}
            return Response(message,status.HTTP_400_BAD_REQUEST)
        
class SelectLocationView(APIView):
    authentication_classes = [JWTUserAuthentication]
    permission_classes = [AllowAny]
    def patch(self,request,id):
        try:
            data=request.data
            user = request.user
            serializer = UpdateUserSerializer(user,data,partial=True)
            if serializer.is_valid():   
                serializer.save()
                print('Location updated successfully')
                response = {
                    'message': 'Location updated successfully',
                    'data' : serializer.data
                }
                return Response(response)
            else:
                print('Location updated failed')
                print(serializer.errors)
                return Response(serializer.error)
            
        except Exception as e:
            raise e
        
        
        
class AllFoodDetails(APIView):
    authentication_classes = [JWTUserAuthentication]
    
    def get(self,request):
        try:
            user = request.user
            food = RestFoodModel.objects.all()
            serializer = RestFoodSerializer(food,many=True)
            print(serializer)
            return Response(serializer.data)
        
        except:
            message = {'detail':'something went wrong'}
            return Response(message,status.HTTP_400_BAD_REQUEST)
        

class AllFoodCategory(APIView):
    authentication_classes = [JWTUserAuthentication]
    
    def get (self,request):
        try:
            user = request.user
            category = Category.objects.all()
            serializer = CategorySerializer(category,many=True)
            return Response(serializer.data)
        except:
            message = {'detail':'something went wrong'}
            return Response(message,status.HTTP_400_BAD_REQUEST)
                
class SetPagination(PageNumberPagination):
    page_size = 2

class PagiantionApi(ListAPIView):
    queryset = RestFoodModel.objects.all()
    serializer_class = RestFoodSerializer
    pagination_class = SetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = {
        'vendor_name': ['exact'],
        'food_name': ['exact'],
        # 'food_category': ['exact'],
        # 'food_description': ['exact'],
        'food_price' : ['exact'],
        
    }
class ItemFilterByPrice(ListAPIView):
    queryset = RestFoodModel.objects.all()
    serializer_class = RestFoodSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ItemFilterByPrice
    
class SearchFood(APIView):
    def get(self,request):
        s = request.GET.get('s')
        food = RestFoodModel.objects.all()
        if s:
            food = RestFoodModel.objects.filter(food_name__icontains=s)
        serializer = RestFoodSerializer(food,many = True)
        return Response(serializer.data)
    
class OrderItemFilterViewSet(ListAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_at']

class OrderItemApiView(APIView):
    authentication_classes = [JWTUserAuthentication]
    serializer_class = OrderSerializer
    
    def post(self,request):
        try:
            userr=request.user
            data = request.data
            request.data_mutable = True
            id = User.objects.get(username=userr).id
            print(id)
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                serializer.save()
                
                response = {
                    'data' : serializer.data,
                    
                }
                return Response(response)
            else:
                return Response(serializer.errors)
        except Exception as e:
            raise e

class ViewOrderItem(APIView):
    authentication_classes = [JWTUserAuthentication]
    serializer_class = OrderItemSerializer
    
    def get(self,request):
        try:
            user = request.user
            data = request.data
            request.data_mutable = True
            id = User.objects.get(username=user).id
            print(id)
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                serializer.save()
                response = {
                    'data' : serializer.data}
                return Response(response)
            else:
                return Response(serializer.errors)
        except Exception as e:
            raise e

class Payment(APIView):
    authentication_classes = [JWTUserAuthentication]
    
    def patch(self,request,id):
        try:
            user = request.user
            data = request.data
            print(user)
            print(data)
            user = User.objects.get(username=user)
            print(id)
            order = Order.objects.get(id=id)
            serializer = PaymentSerializer(order,data)
            if serializer.is_valid():
                serializer.save()
                print(serializer.data)
                response = {
                    'message' : 'payment proccessing on razorpay'
                }
                return Response(response)
            else:
                print(serializer.errors)
                return Response(serializer.errors)
        except Exception as e:
            raise e
@csrf_exempt      
def temp_payment(request):
    amount = 0
    payment = 0
    if request.method == 'POST':
        amount = request.POST.get('amount')
        id = request.POST['order_number']
        request.session['key'] = id
        print(id)
        print(amount)
        
        client =razorpay.Client(auth=(settings.RAZORPAY_PUBLIC_KEY,settings.RAZORPAY__SECRET_KEY))
        print(client)
        payment = client.order.create({"amount": int(amount) * 100, 
                                   "currency": "INR", 
                                   "payment_capture": "1"})
        print(payment)
        order = Order.objects.get(id=id)
        print(order)
   
        print(payment['id'])
     
        
        return render(request,'payments.html',{'payment':payment,'order':order})
    return render(request,'payments.html')

@csrf_exempt
def payment_status(request):
    status = None
    response = request.POST
    print(response)
    params_dict = {
            'razorpay_order_id':response['razorpay_order_id'],
            'razorpay_payment_id':response['razorpay_payment_id'],
            'razorpay_signature':response['razorpay_signature']
        }
    print(params_dict)
    print('response=',response)
    client = razorpay.Client(auth = (settings.RAZORPAY_PUBLIC_KEY,settings.RAZORPAY__SECRET_KEY))
    print(client)
    status = client.utility.verify_payment_signature(params_dict)
    print(status)

    try:
        id = request.session['key']
        user = User.objects.get(id=id)
        user.payment_id = response['razorpay_payment_id']
        print(user.payment_id,'payment_id')
        serializer = PaymentSerializer(user,partial=True)
        print(serializer)
        for i in serializer.data:
           order = Order.objects.get(order_number=i)
           order.payment_status = True
           print(order.payment_status)
           order.save()
        
        id = request.session['key']
        order = Order.objects.get(id=id)
        
        order.payment_status = True
        order.save()
        
        
        
        return render(request,'success.html',{'status':True})
    
    except PaymentError as e:
         return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    except PaymentCancelled as e:
         return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
     
    except PaymentTimeout as e:
          return Response({"error": str(e)}, status=status.HTTP_408_REQUEST_TIMEOUT)
      
    except SignatureVerificationError as e:
         return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
    
    except OrderNotFoundError as e:
         return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
     
     
class TrackUserOrders(APIView):
    authentication_classes = [JWTUserAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request,id):
        user_id = request.user
        print(user_id)
        orders = OrderItem.objects.filter(user_id=user_id)
        serializer = OrderItemSerializer(orders,many=True)
        return Response(serializer.data)
    
            
        


          

        
        
        
    
