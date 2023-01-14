from django.db import models

# Create your models here.
class District(models.Model):
    district = models.CharField(max_length=100,unique=True)
    
    def __str__(self):
        return self.district
    
class City(models.Model):
    district = models.ForeignKey(District,on_delete=models.CASCADE)
    city = models.CharField(max_length=200)
    
    def __str__(self):
        return self.city
    
class Category(models.Model):
    category_name = models.CharField(max_length=225,unique=True)
    slug = models.SlugField(max_length=100,unique=True)
    
    class Meta:
        verbose_name = 'category_name'
        verbose_name_plural = 'categories'
        
class Menu(models.Model):
    Restaurant_id = models.CharField(max_length=225,null=True,blank=True)
    food_name = models.CharField(max_length=225,null=True,blank=True)
    category_name = models.ManyToManyField(Category)
    
    
    
    