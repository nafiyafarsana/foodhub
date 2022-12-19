from django.shortcuts import render
import datetime


from rest_framework.views import APIView
from rest_framework import authentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer



# Create your views here.


class VendorRegister(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [AllowAny]
    
    
    def post(self,request):
        serializer = AuthTokenSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        
        
        
        
        
    
    