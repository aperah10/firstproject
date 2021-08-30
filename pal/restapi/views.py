from django.shortcuts import render
from rest_framework.generics import ListAPIView ,CreateAPIView ,RetrieveAPIView ,ListCreateAPIView ,RetrieveUpdateDestroyAPIView
from rest_framework.authentication import BaseAuthentication 
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly,AllowAny
from rest_framework.authentication import TokenAuthentication  
from rest_framework.views import APIView
from django.db.models import Q 
from rest_framework.response import Response 
from django.contrib.auth.hashers import make_password

from django.views.generic import TemplateView 
from rest_framework.status import (
    HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK)
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes 

from rest_framework.filters import SearchFilter

# MY IMPORTS FOR ALL FILES   
from accounts.models import *
from product.models import *
from .serializer import *

 # ! PRODUCT SEARCH BAR 
class SrchProduct(ListAPIView):
    # queryset = Product.objects.all()
    # serializer_class = AllProductSer 
    # search_fields=['title', 'description']
    queryset=CustomUser.objects.all()
    serializer_class=AccountsSeri
    filter_backends=[SearchFilter]
    search_fields=['fullname', 'phone']
#     # ! this is used in Filter 
#     # filter_backends = [DjangoFilterBackend]
#     # filterset_fields = ['title', 'description']


# Create your views here.
#  HOME PAGE 
class HomePage(TemplateView):
    template_name='restapi/Home.html'






# GET DATA API 
class DataGet(ListAPIView):
    # permission_classes=[IsAuthenticated,] 
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
            user = serializer.save()
            username = data.get('phone')
            raw_password = data.get('password')
            
            cur_user = authenticate(username=username, password=raw_password)
           
           
            token, _ = Token.objects.get_or_create(user=cur_user)
            return Response({"stateCode": 200, "msg": "enter data",'token': token.key,}, 200)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


# =============================== LOGIN   =====================================
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("phone")
    password = request.data.get("password")
    # if username is None or password is None:
    #     return Response({'error': 'Please provide both username and password'},
    #                     status=HTTP_400_BAD_REQUEST)
    # user = authenticate(username=username, password=password)
    try:
        user = authenticate(username=CustomUser.objects.get(
            email__iexact=username), password=password)

    except:
        user = authenticate(username=username, password=password)

    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)





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


#  #  PRODUCT SEARCH BAR 
# class SearchProduct(generics.ListAPIView):

#     queryset = Product.objects.all()
#     serializer_class = AllProductSer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['title', 'description']



#  =======================GET DATA  SECTION =================================
# SHOW ALL PRODUCT 
class AllProduct(ListAPIView):
    queryset =Product.objects.all()
    serializer_class= AllProductSer 

   
            
# CART FOR USER 
class GetCart(APIView):
    permission_classes=[IsAuthenticated] 

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

  
# # SERACH PRODUCT 
# class SearchResultsView(ListView):
#     model = Product
    
#     #prod=Product.objects.all()

#     def get_queryset(self):
#         query = self.request.GET.get('search')
#         products=Product.objects.filter(Q(title__icontains=query))
#         return products
    
