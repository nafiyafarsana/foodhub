from django.db import models
from django.contrib.auth.models import BaseUserManager     


     


# Create your models here.


        
class Vendor(models.Model):
    
    vendor_name    = models.CharField(max_length=100, unique=True,null=True)
    email          = models.EmailField(max_length=100, unique=True)
    phone_number   = models.CharField(max_length=100,unique=True)
    password       = models.CharField(max_length=100)
    address        = models.CharField(max_length=100,null=True)
    location       = models.CharField(max_length=100,null=True)
    license        = models.CharField(max_length=100,null=True,blank=True)
    
    #required
    # date_joined    = models.DateTimeField(auto_now_add=True,null=True)
    # last_login     = models.DateTimeField(auto_now_add=True,null=True)
    is_admin       = models.BooleanField(default=False)
    is_staff       = models.BooleanField(default=False)
    is_active      = models.BooleanField(default=False)
    is_superuser   = models.BooleanField(default=False)
    is_vendor      = models.BooleanField(default=True)
    
    
    
    USERNAME_FIELD  = 'vendor_name'
    REQUIRED_FIELDS = ['email','phone_number']

    
    
    
    def __str__(self):
        return self.email
    
    @property
    def is_anonymous(self):
        """
        Always return False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

 
    @property
    def is_authenticated(self):
        """
        Always return False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    

class VendorToken(models.Model):
    vendor_id = models.IntegerField()
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()

    def __str__(self):
        return str(self.vendor_id) +' '+ self.token
    

class RestMenuModel(models.Model):
    vendor_name = models.OneToOneField(Vendor,on_delete=models.CASCADE,primary_key=True)
    Menu = models.CharField(max_length=3000)
    special_items = models.CharField(max_length=3000,null=True,blank=True)
    offer = models.CharField(max_length=3000,null=True,blank=True)
    veg = models.BooleanField(null=True,blank=True)
    non_veg = models.BooleanField(null=True,blank=True)
    cover_photo = models.ImageField(upload_to='pictures/%Y/%m/%d/',max_length=2000,blank=True,null=True)
    
    def __str__(self):
        return self.special_items
    
    
class RestFoodModel(models.Model):
    vendor_name = models.ManyToManyField(Vendor)
    Menu = models.OneToOneField(RestMenuModel,on_delete=models.CASCADE,null=True)
    food_name = models.CharField(max_length=3000)
    food_image = models.ImageField(upload_to='pictures/%Y/%m,/%d/',max_length=3000,null=True,blank=True)
    food_category = models.CharField(max_length=3000,null=True,blank=True)
    food_description = models.TextField(max_length=3000,null=True,blank=True)
    food_prize = models.PositiveIntegerField()
    slug = models.SlugField(max_length=225,unique=True,null=True)
    
    def __str__(self):
        return self.food_name
    
class AddTime(models.Model):
    opening_time = models.TimeField(null=True)
    closing_time = models.TimeField(null=True)
    

    
    

    
    
    
    
    
    

   
    
    
    
    

    
   
    


