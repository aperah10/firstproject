from django.urls import path
from . import views 
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns =[

    # ========== THIS IS HOME PAGE ==========
    path('',views.HomePage.as_view(),name='home'),

    path('reg/', views.DataGet.as_view(),name='getdata') ,
    path('rud/<uuid:pk>/', views.DataRUD.as_view(),name='rud') ,
    path('profile/<uuid:pk>/',views.ProfileRUD.as_view(),name='profilerud'), 

    # ==========POST REQUEST FOR ==================
    path('login/', obtain_auth_token),
    path('crusr', views.PostRegister.as_view(),name='postdata') ,
    path('crcart/',views.PostCart.as_view(),name='postcart'),
    path('crlike/',views.PostLike.as_view(),name='postlike'),
    path('crnoti/',views.PostNoti.as_view(),name='postnoti'),  
    
  
    # ============ GET REQUEST FOR ALL ===========================  
    path('p/',views.AllProduct.as_view(),name='product'), 
    path('cart/',views.GetCart.as_view(),name='cart') ,
    path('like/',views.GetLike.as_view(),name='like'),
    path('noti/',views.GetNoti.as_view(),name='noti') , 

    # ================DELETE DATA ===============
    path('delcart/',views.DeleteCart.as_view(),name='delcart') ,
    path('delnoti/',views.DeleteNoti.as_view(),name='delnoti') ,
    path('dellike/',views.DeleteLike.as_view(),name='dellike') ,




]