from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.VendorRegister.as_view(),name='vendor_register'),
]
