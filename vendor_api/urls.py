from django.urls import path
from . import views

urlpatterns = [
    path('vendor_register/',views.VendorRegister.as_view(),name='vendor_register'),
    path('vendor_login/',views.VendorLogin.as_view(),name='vendor_login'),
    path('vendor/',views.VendorAPIView.as_view(),name='vendor'),
    path('MenuUpload/<int:id>/',views.UploadMenuAPIView.as_view(),name='MenuUpload'),
    path('Food_details/<int:id>/',views.FoodDetailView.as_view(),name='Food_details'),
    path('vendor_logout/',views.VendorLogoutApiView.as_view(),name='vendor_logout'),
    
    
    path('restaurant_time/',views.AddRestTime.as_view(),name='restaurant_time'),
    path('update_menu/<int:id>/',views.UpdateMenu.as_view(),name='update_menu'),
    path('get_menu/<int:id>',views.GetAllMenu.as_view(),name='get_menu'),
    path('Add_food/',views.AddFood.as_view(),name='Add_food'),
    path('Ban_food/<int:id>/',views.BanFood.as_view(),name='Ban_food'),


]
