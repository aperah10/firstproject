from django.urls import path
from . import views 

urlpatterns =[
    path('reg/', views.DataGet.as_view(),name='getdata') ,
    path('rud/<uuid:pk>/', views.DataRUD.as_view(),name='rud') ,
    path('profile/<uuid:pk>/',views.ProfileRUD.as_view(),name='profilerud'), 

    # ==========POST REQUEST FOR ==================
    path('', views.PostRegister.as_view()) ,
    path('crcart/',views.PostCart.as_view()),
    path('crlike/',views.PostLike.as_view()),
    path('crnoti/',views.PostNoti.as_view()),  
    
  
    # ============ GET REQUEST FOR ALL ===========================  
    path('p/',views.AllProduct.as_view(),name='prodcut'), 
    path('cart/',views.GetCart.as_view()) ,
    path('like/',views.GetLike.as_view()),
    path('noti/',views.GetNoti.as_view()) , 

    # ================DELETE DATA ===============
    path('delcart/',views.DeleteCart.as_view()) ,
    path('delnoti/',views.DeleteNoti.as_view()) ,
    path('dellike/',views.DeleteLike.as_view()) ,




]