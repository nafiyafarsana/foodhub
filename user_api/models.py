from django.db import models
from vendor_api.models import RestFoodModel
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin     
# from django.core.validators import RegexValidator

# Create your models here.


# class User(AbstractUser):
#     username = models.CharField(max_length=64,unique=True)
#     email =  models.EmailField(unique=True)
#     phone_number = models.CharField( max_length=15, unique=True)
#     password = models.CharField(max_length=200)
#     address = models.TextField()
    

#     def __str__(self):
#         return self.username


class myAccountManager(BaseUserManager):
    def create_user(self, username,email,phone_number, password=None):
        if not email:
            raise ValueError('User must have an email address')
    
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            phone_number = phone_number, 
        
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    
    def create_superuser(self, username,email,phone_number, password):
        user = self.create_user(
            email = self.normalize_email(email),
            password = password,
            username = username,
            phone_number = phone_number,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser =True
        user.save(using=self.db)
        return user
        
class User(AbstractBaseUser,PermissionsMixin):
    
    username       = models.CharField(max_length=100, unique=True)
    email          = models.EmailField(max_length=100, unique=True)
    phone_number   = models.CharField(max_length=100,unique=True)
    address        = models.CharField(max_length=100,null=True)
    location   = models.CharField(max_length=100,null=True)
    
    #required
    # date_joined    = models.DateTimeField(auto_now_add=True)
    # last_login     = models.DateTimeField(auto_now_add=True)
    is_admin       = models.BooleanField(default=False)
    is_staff       = models.BooleanField(default=False)
    is_active      = models.BooleanField(default=True)
    is_superuser  = models.BooleanField(default=False)

   
    
      
    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS = ['email','phone_number']
    
    

    objects = myAccountManager()
    
    class Meta:
        verbose_name ='user'
        verbose_name_plural = 'users'
        
     
    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True    
    

class UserToken(models.Model):
    user_id = models.IntegerField()
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()
    
class PaymentModel(models.Model):
    username = models.ForeignKey(User,on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100,null=True)
    order_id = models.CharField(max_length=100,null=True,blank=True)
    order_number = models.CharField(max_length=100,null=True,blank=True)
    payment_method = models.CharField(max_length=100,null=True,default='Razorpay')
    amount_paid = models.CharField(max_length=100,default=0)
    status = models.CharField(max_length=100,default='not_paid')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.username)
    

class Order(models.Model):
    
    username = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    # payment = models.ForeignKey(PaymentModel,on_delete=models.SET_NULL,blank=True,null=True)
    # order_number = models.CharField(max_length=20)
    username = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=20)
    location = models.CharField(max_length=20)
    order_total = models.FloatField()
    tax = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_status = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.username) 
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,null=True,blank=True)
    # payment = models.ForeignKey(PaymentModel,on_delete=models.CASCADE,blank=True,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    food_item = models.ForeignKey(RestFoodModel,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    food_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.food_item.food_name
    
    
    
    

