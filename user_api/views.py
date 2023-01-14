from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework import generics

from . models import User,UserToken
from . serializers import UserSerializer
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

            print('*')
            if user:
                print('jj',user,user.id)
                access_token = create_access_token(user.id)
                print('ll')
                print(access_token)
                refresh_token = create_refresh_token(user.id)
                print('aaaaaa')
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

# class SendOtp(APIView):
#     def post(self,request):
#         account_sid = settings.TWILIO_ACCOUNT_SID
#         auth_token = settings.TWILIO_AUTH_TOKEN
#         phone_number = request.data['phone_number']
#         client = Client(account_sid,auth_token)
#         otp = generateOTP()
#         body = 'Your OTP is' + str(otp)
#         message = client.messages.create(from_='+12069443948',body=body,to=phone_number)
#         if message.sid:
#             print('send successfull')
#             return JsonResponse({'success':True})
#         else:
#             print('send fail')
#             return JsonResponse({'success':False})
# def generateOTP():
#     return random.randrange(100000,999999)

# class VerifyUserOtp(APIView):
#     permission_classes = [AllowAny]
#     serializer_class = UserSerializer
#     def post(self,request):
#         otp = request.data['otp']
#         phone_numnber = request.data['phone_number']
#         stored_otp = User.objects.get(phone_numnber=phone_numnber)
#         if otp == stored_otp:
#             return JsonResponse({'success':True})
#         else:
#             return JsonResponse({'status': False})



class LoginUserWithOtpAPIView(APIView):
    def post(self, request):
        """ required field : phone_number-10 digit number """
        try:
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
                print('-----------')
                response = Response()
                print('--------------')
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
        except:
            message = {'detail':'somthing went wrong'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

class VerifyLoginUserOtp(APIView):
    def post(self,request):

        """ required field : code - string"""
        try:
            data=request.data
            print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
            phone_number=request.COOKIES.get('phone_number')
            print(phone_number)
            code=data['code']
            print(code)
            if check(phone_number,code):
                user = User.objects.filter(phone_number=phone_number).first()
                print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
                print(user)
                print(user)
                if user:
                    print('-------------------------------')
                    # response.delete_cookie(key='phone_number')
                    access_token = create_access_token(user.id)
                    refresh_token = create_refresh_token(user.id)
                    print('-------------------------------')
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
            print(user)
            category = Category.objects.all()
            serializer = CategorySerializer(category,many=True)
            return Response(serializer.data)
        except:
            message = {'detail' : 'something went wrong'}
            return Response(message,status.HTTP_400_BAD_REQUEST)
        
class SelectLocationView(APIView):
    authentication_classes = [TokenAuthenticationSafe]
    # permission_classes = [AllowAny]
    def patch(self,request,id):
        try:
            data=request.data
            user = request.user
            print(user)
            print('lkkjfknfj')
            user = User.objects.filter(user = user).id
            print('NNNNNNNNNNNNNNNN')
            print(user)
            serializer = UpdateUserSerializer(user,data,partial=True)
            print(serializer)
            if serializer.is_valid():
                print('hhhhhhhhhhhh')
                serializer.save()
                print('bbbbbbbbbb')
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
            
        except:
            message = {'detail':'something went wrong'}
            return Response(message,status.HTTP_400_BAD_REQUEST)
        
        
        
class AllFoodDetails(APIView):
    # authentication_classes = [JWTUserAuthentication]
    
    def get(self,request):
        try:
            user = request.user
            print(user)
            print('sssssssssss')
            food = RestFoodModel.objects.all()
            print('jjjjjjjj')
            serializer = RestFoodSerializer(food,many=True)
            print('kkkkkkkkkkk')
            print(serializer)
            return Response(serializer.data)
        
        except:
            message = {'detail':'something went wrong'}
            return Response(message,status.HTTP_400_BAD_REQUEST)
        
# class SearchByCategory(generics.ListAPIView):
    
#     queryset = RestFoodModel.objects.all()
#     filter_backends = [DjangoFilterBackend]
#     serializer_class = RestFoodSerializer
#     authentication_classes = [JWTUserAuthentication]
#     permission_classes = [IsAuthenticated]
#     filter_backends = (SearchFilter,OrderingFilter)
#     search_fields = ('food_name','food_category','Vendor__location')

class AllFoodCategory(APIView):
    authentication_classes = [JWTUserAuthentication]
    
    def get (self,request):
        try:
            user = request.user
            print(user)
            
            category = Category.objects.all()
            serializer = CategorySerializer(category,many=True)
            return Response(serializer.data)
        except:
            message = {'detail':'something went wrong'}
            return Response(message,status.HTTP_400_BAD_REQUEST)
        




            
            

        
        
        
    
