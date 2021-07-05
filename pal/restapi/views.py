from django.shortcuts import render
from rest_framework.generics import ListAPIView ,CreateAPIView ,RetrieveAPIView ,ListCreateAPIView ,RetrieveUpdateDestroyAPIView
from rest_framework.authentication import BaseAuthentication 
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication  
from rest_framework.views import APIView
from django.db.models import Q 
from rest_framework.response import Response 
from django.contrib.auth.hashers import make_password


# MY IMPORTS FOR ALL FILES   
from accounts.models import *
from product.models import *
from .serializer import *

# Create your views here.




# GET DATA API 
class DataGet(ListAPIView):
    permission_classes=[IsAuthenticated,] 
    queryset= CustomUser.objects.all()
    serializer_class= AccountsSeri 


# # UPDATE AND DESTROY AND GET  USER DATA 
class DataRUD(RetrieveUpdateDestroyAPIView):
    queryset=CustomUser.objects.all()
    serializer_class=AccountsSeri
    permission_classes=[IsAuthenticated,] 

class ProfileRUD(RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAuthenticated,] 
    authentication_classes = [TokenAuthentication, ] 

    queryset =Profile.objects.all() 
    serializer_class = ProfileSeri 


# POST DATA FOR CREATE USER 
class PostRegister(APIView):

    def post(self, request, format=None):
        data = request.data
        # if CustomUser.objects.filter(username__exact=data.get('username')):
        #     return Response({"stateCode": 201, "msg": "User Exits"}, 201)
        # if CustomUser.objects.filter(email__exact=data.get('email')):
        #     return Response({"stateCode": 202, "msg": "User enn"}, 201)
        new_user = {
            'fullname': data.get('fullname'),
            'phone': data.get('phone'),
            'email': data.get('email'),
            'password': make_password(data.get('password')),
            
        }
        # print(new_user)
        serializer = AccountsSeri(data=new_user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"stateCode": 200, "msg": "enter data"}, 200)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    

# nrw cart post for check 
class PostCart(CreateAPIView):
    permission_classes=[IsAuthenticated] 

    queryset = ProductInCart.objects.all()
    serializer_class=CartSer  

# NEW LIKE  post for check 
class PostLike(CreateAPIView):
    permission_classes=[IsAuthenticated] 

    queryset = Like.objects.all()
    serializer_class=LikeSer  

# NEW  NOTITFICATION  POST  FOR 
class PostNoti(CreateAPIView):
    permission_classes=[IsAuthenticated] 

    queryset = Notification.objects.all()
    serializer_class=NotificationSer   





#  =======================GET DATA  SECTION =================================
# SHOW ALL PRODUCT 
class AllProduct(ListAPIView):
    queryset =Product.objects.all()
    serializer_class= AllProductSer 

   
            
# CART FOR USER 
class GetCart(APIView):
    # permission_classes=[IsAuthenticated] 

    def get(self,request):
        usr= request.user 
        usr_cart =ProductInCart.objects.filter(customer_cart=usr) 
        
        try:
            ser=CartSer(usr_cart,many=True)   
            alldata=ser.data
            
        except:
            alldata=ser.errors
        return Response(alldata) 
    


 
# LIKE OF USER 
class GetLike(APIView):
    permission_classes=[IsAuthenticated] 

    def get(self,request):
        usr= request.user
        usr_like =Like.objects.filter(user=usr)
       
        try: 
            ser=LikeSer(usr_like,many=True) 
            alldata=ser.data
           
            
        except:
            alldata=ser.errors
          
        return Response(alldata)


# # MAKING NOTIFICATION 
class GetNoti(APIView):
    permission_classes=[IsAuthenticated] 
   
    def get(self,request):
        usr=request.user 
        noti=Notification.objects.filter(user=usr)
        
        try:
            ser=NotificationSer(noti,many=True) 
            alldata=ser.data
            
        except:
            alldata=ser.errors
           
        return Response(alldata)



 #=========================DELETE ================= 
class DeleteCart(APIView):
    permission_classes = [IsAuthenticated, ]
 
    def post(self,request):  
        prod=request.data['product'] 
        cus=request.data['customer_cart']
     
        try:
            if ProductInCart.objects.filter(Q(customer_cart=cus) & Q(product=prod)).exists():
              pod= ProductInCart.objects.filter(Q(customer_cart=cus) & Q(product=prod))
              print(pod)
              pod.delete() 
              res = {'error': False,'msg':'data delete'} 
            else: 
                res = {'error': True,'msg':' not have any data'}  
        
        except: 
            res = {'error': True}
        return Response(res)


# # DELETE FOR LIKE 
   
class DeleteLike(APIView):
    permission_classes = [IsAuthenticated, ]
 
    def post(self,request):  
        prod=request.data['product'] 
        cus=request.data['user']
   
        try:
            if Like.objects.filter(Q(user=cus) & Q(product=prod)).exists():
              pod= Like.objects.filter(Q(user=cus) & Q(product=prod))
              print(pod)
              pod.delete() 
              res = {'error': False,'msg':'data delete'} 
            else: 
                res = {'error': True,'msg':' not have any data'}  
        
        except: 
            res = {'error': True}
        return Response(res)


# DELETE FOR NOTITFICATION
   
class DeleteNoti(APIView):
    permission_classes = [IsAuthenticated, ]
 
    def post(self,request):  
        prod=request.data['product'] 
        cus=request.data['user']
        sender=request.data['sender']
      
        try:
            if Notification.objects.filter(Q(Q(user=cus) & Q(product=prod)) & Q(Q(user=cus) & Q(sender=sender) )).exists():
              pod= Notification.objects.filter(Q(Q(user=cus) & Q(product=prod)) & Q(Q(user=cus) & Q(sender=sender) ))
              print(pod)
              pod.delete() 
              res = {'error': False,'msg':'data delete'} 
            else: 
                res = {'error': True,'msg':' not have any data'}  
        
        except: 
            res = {'error': True}
        return Response(res)

         
    