from django.urls import path
from . import views

urlpatterns = [
    path('user_register/',views.UserRegister.as_view(),name='user_register'),
    path('user_login/',views.UserLogin.as_view(),name='user_login'),
    path('user/',views.UserAPIView.as_view(),name='user'),
    path('SendOtp/',views.LoginUserWithOtpAPIView.as_view(),name='SendOtp'),
    path('VerifyOtp/',views.VerifyLoginUserOtp.as_view(),name='VerifyOtp'),
    path('user_logout/',views.UserLogoutApiView.as_view(),name='user_logout'),
    path('all_categories/',views.AllCategories.as_view(),name='all_categories'),
    path('select_location/<int:id>/',views.SelectLocationView.as_view(),name='select_location'),
    path('All_food/',views.AllFoodDetails.as_view(),name='All_food'),
    # path('Search/',views.SearchByCategory.as_view(),name='Search'),
    path('All_food_category/',views.AllFoodCategory.as_view(),name='All_food_category'),
    path('PagiantionApi/',views.PagiantionApi.as_view(),name='PagiantionApi'),\
    path('ItemFilterByPrice/',views.ItemFilterByPrice.as_view(),name='ItemFilterByPrice'),
    path('SearchFood/',views.SearchFood.as_view(),name='SearchFood'),



    path('trackorder/<int:id>/',views.TrackUserOrders.as_view(),name='trackorder'),
    path('ViewOrderItem/',views.ViewOrderItem.as_view(),name='ViewOrderItem'),
    path('OrderItem/',views.OrderItemApiView.as_view(),name='OrderItem'),
    path('OrderItemfilterview/',views.OrderItemFilterViewSet.as_view(),name='OrderItemfilterview'),
    path('payment/<int:id>/',views.Payment.as_view(),name='payment'),
    path('temp_payment/',views.temp_payment,name='temp_payment'),
    path('payment_status/',views.payment_status,name='status'),


    

    
    
    



    



  

]
