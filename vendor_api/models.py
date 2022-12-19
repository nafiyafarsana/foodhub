from django.db import models

# Create your models here.

class Vendor(models.Model):
    restaurant_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100,unique=True)
    phone_number = models.CharField(max_length=15,unique=True)
    password = models.CharField(max_length=100)
    
    
    create_date = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_vendor = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False,blank=True)
    
    
    def __str__(self):
        return self.email
    
