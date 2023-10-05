
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authentication import get_authorization_header
from rest_framework import generics 

from . models import Vendor,VendorToken,RestMenuModel,RestFoodModel
from .serializer import VendorSerializer,RestMenuSerializer,RestFoodSerializer,AddRestTimeSerializer

import datetime
from .authentication import JWTVendorAuthentication,create_access_token,create_refresh_token,decode_access_token,decode_refresh_token
from django.contrib.auth.hashers import check_password

from django.conf import settings
from django.db.models import Q
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.parsers import FormParser,MultiPartParser,JSONParser

from .myauth import TokenAuthenticationSafe

# Create your views here.

class VendorRegister(APIView):
    permission_classes = [AllowAny]
    serializer_class = VendorSerializer
    
    def post(self,request):
        data = request.data
        serializer = self.serializer_class(data=data)
        
        
        if serializer.is_valid():
            serializer.save()
            
            response = {
                "messages" : "Vendor created succesfully",
                "data" : serializer.data
            }
            
            return Response (data=response,status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class VendorLogin(APIView):
    def post(self,request):
        try:
            email = request.data['email']
            givenpassword = request.data['password']

            vendor = Vendor.objects.get(email=email)
            print(vendor)
            if vendor is None:
                response = Response()
            
                response.data={
                    'message':'Invalid email'
                }
                return response
             

          
            storedpassword = str(vendor.password)

            ans = check_password(givenpassword, storedpassword)
            print(ans)


            if  not check_password(givenpassword, storedpassword) :
                response = Response()
                response.data={
                'message':'Password Inncorect'
                }
                return response  

            if vendor.is_active:
                access_token = create_access_token(vendor.id)
                refresh_token = create_refresh_token(vendor.id)
                print(vendor)

                VendorToken.objects.create(
                    vendor_id = vendor.id,
                    token= refresh_token,
                    expired_at =  datetime.datetime.utcnow()+datetime.timedelta(seconds=7),
                )

                response = Response()
                
                response.set_cookie(key='refresh_token',value=refresh_token,httponly=True)
                response.data = {
                    'token': access_token,
                    
                }
                return response
            else:
                response = Response()
                response.data={
                    'message':'Not verifiede vendor'
                }
                return response  
        except:
            message = {'detail':'somthing went worng'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        

class VendorAPIView(APIView):
    authentication_classes = [JWTVendorAuthentication]
    def get(self,request):
        try:
            return Response(VendorSerializer(request.user).data)
        except:
            message = {'detail':'somthing went wrong'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        

class VendorLogoutApiView(APIView):
    def post(self,request):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            VendorToken.objects.filter(token=refresh_token).delete()
            response = Response()
            response.delete_cookie(key='refresh_token')
            response.data = {
                'message' : 'Vendor Logout Successfully '
            }
            return response
        except:
            message = {'detail':'soumething went wrong'}
            return response(message,status.HTTP_400_BAD_REQUEST)

    

class UploadMenuAPIView(APIView):
    authentication_classes = [TokenAuthenticationSafe]
    parser_classes = [JSONParser,FormParser,MultiPartParser]
    
    def post(self,request,id):
        try:
            data = request.data
            serializer = RestMenuSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                
                print(serializer.data)
                
                response={
                    "data" : serializer.data
                }
                return Response(response)
            else:
                print(serializer.errors)
                return Response(serializer.errors)
        except:
            message = {'detail':'somthing whent worng'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


class FoodDetailView(APIView):
    authentication_classes =[JWTVendorAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self,request,id):
        try:
            data = request.data
            serializer = RestFoodSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                
                print(serializer.data)
                
                response = {
                    "data" : serializer.data
                }
                return Response(response)
            else:
                print(serializer.errors)
                return Response(serializer.errors)
            
        except:
             message = {'detail':'somthing whent worng'}
             return Response(message, status=status.HTTP_400_BAD_REQUEST)
         

class AddRestTime(APIView):
    # authentication_classes = [JWTVendorAuthentication]
    def post(self,request):
        try:
            data = request.data
            serializer = AddRestTimeSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                
                response = {
                    'data' : serializer.data
                }
                return Response(response)
            else:
                print(serializer.errors)
                return Response(serializer.errors)
            
        except:
            message = {'detail':'something went wrong'}
            return Response(message,status.HTTP_400_BAD_REQUEST)
            
            
class UpdateMenu(APIView):
    authentication_classes = [JWTVendorAuthentication]
    
    def get_queryset(self):
        menu = RestMenuModel.objects.all()
        return menu
    
    def patch(self,request,id):
        try:    
            data = request.data
            request.data_mutable = True
            vendor =request.user
            data['vendor'] = vendor
            data.update(request.data)
            menu = RestMenuModel.objects.get(vendor_name=id)
            if menu.vendor_name == vendor:
                serializer = RestMenuSerializer(menu,data=request.data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    print('Menu update Successfully')
                    return Response(serializer.data)
                else:
                    print(serializer.errors)
                    return Response(serializer.errors)
            else:
                response = {
                    'message' : 'You are not allowed for this action'
                }
                return Response(response)
        except Exception as e:
             raise e
           
        
    def put(self,request,id):
        try:
            data = request.data
            request.data_mutable = True
            vendor =request.data
            id2 = Vendor.objects.all()
            data['vendor'] = id2
            data.update(request.data)
            menu = RestMenuModel.objects.all()
            print(vendor)
            # print(menu)
            if menu.vendor == vendor:
                serializer = RestMenuSerializer(menu,data=request.data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    print('Menu update Successfully')
                    return Response(serializer.data)
                else:
                    print(serializer.errors)
                    return Response(serializer.errors)
            else:
                response = {
                    'message' : 'You are not allowed for this action'
                }
                return Response(response)
        except:
            message = {'detail' :'something went wrong'}
            return Response(message,status.HTTP_400_BAD_REQUEST)
            
            
class GetAllMenu(APIView):
    authentication_classes = [JWTVendorAuthentication]
    def get(self,request,id):
        try:
            vendor = request.user
            menu = RestMenuModel.objects.filter(vendor_name=vendor)
            serializer = RestMenuSerializer(menu,many=True)
            print(serializer)
            return Response(serializer.data)
        except Exception as e:
           raise e
        
class AddFood(APIView):
    authentication_classes = [JWTVendorAuthentication]
    def post(self,request):
        try:
            data = request.data
            print(data)
            # request.data_mutable = True
            # data.update(request.data)
            serializer = RestMenuSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                print(serializer.data)
                response = {
                    'data' : serializer.data
                }
                return Response(response)
            else:
                print(serializer.errors)
                return Response(serializer.errors)
        except Exception as e:
           raise e
        
class BanFood(APIView):
    authentication_classes = [JWTVendorAuthentication]
    permission_classes = [IsAuthenticated]
    
    def patch(self,request,id):
        try:
            food = RestFoodModel.objects.get(id=id)
            vendor = request.user
            print(vendor)
            if vendor == food.vendor:
                if food.is_active == True:
                    food.is_active = False
                else:
                    food.is_active = True
                print(food.is_active)
                
                serializer = RestFoodSerializer(food,data=request.data,partial=True)
                if serializer.is_valid:
                    serializer.save()
                    print("food banned successfully")
                    return Response(serializer.data)
                else:
                    print('your action failed')
                    print(serializer.errors)
                    return Response(serializer.errors)
                
        except Exception as e:
            raise e

                
            
            
        
                
               
            
            

    
        