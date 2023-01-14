from django.contrib import admin
from .models import Vendor,VendorToken,RestFoodModel,RestMenuModel

# Register your models here.

admin.site.register(Vendor)
admin.site.register(VendorToken)
admin.site.register(RestMenuModel)
admin.site.register(RestFoodModel)

