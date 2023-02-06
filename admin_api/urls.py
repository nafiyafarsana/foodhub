from django.urls import path
from . import views


urlpatterns = [
     path('verifyvendor/<int:id>/',views.VerifyVendor.as_view(),name='verifyvendor'),
     path('VendorAllList/',views.VendorAllList.as_view(),name='VendorAllList'),
     path('VendorDetailsView/<int:id>/',views.VendorDetailsView.as_view(),name='VendorDetailsView'),
     path('BlockVendor/<int:id>/',views.BlockVendor.as_view(),name='BlockVendor'),
     
     
     path('userslist/',views.UsersListView.as_view(),name='userslist'),
     path('userdetailview/<int:id>/',views.UsersDetailsView.as_view(),name='userdetailview'),
     path('BlockUser/<int:id>/',views.BlockUser.as_view(),name='BlockUser'),
     
     
     path('Add_category/<int:id>/',views.AddcategoryView.as_view(),name='Add_category'),
     path('Add_food/',views.AddFoodView.as_view(),name='Add_food'),
     path('Block_food/<int:id>/',views.BlockFoodView.as_view(),name='Block_food'),
     path('update_food/<int:id>/',views.UpdateFood.as_view(),name='update_food'),
     path('food_details/',views.FoodDetails.as_view(),name='food_details'),
     path('GetAllPaidOrders/',views.GetAllPaidOrders.as_view(),name='GetAllPaidOrders'),

     

     


     
     



]
