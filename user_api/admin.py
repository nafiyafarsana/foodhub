from django.contrib import admin
from .models import User,UserToken,Order,OrderItem,PaymentModel

# Register your models here.

admin.site.register(User)
admin.site.register(UserToken)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(PaymentModel)
