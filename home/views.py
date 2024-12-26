from datetime import datetime, timedelta

import jwt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.authtoken.models import Token # for generating token if user is doing login
from django.contrib.auth import authenticate 
from django.contrib.auth import get_user_model

from .authentication import JwtAuthentcation, Dispatch
from django_ecommerce import settings
from .models import *
from .serializer import *

User = get_user_model()


class RegisterUser(APIView):
    def post(self, request):
        data = request.data
        print('______________________________________________',data)
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'User Register sucessfully'},status=status.HTTP_201_CREATED)
        else:
            print('serializer error')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class LoginUser(APIView):
    def post(self , request):
        data = request.data
        serializer = LoginSerializer(data=data)
        if serializer.is_valid():
            is_authenticated = authenticate(username=serializer.data['username'], password=serializer.data['password'])

            if is_authenticated: # always return token in str(token) way
                # token, _ = Token.objects.get_or_create(user=is_authenticated)
                # return Response({'message':'login sucessfull' , 'Token':str(token)}, status= status.HTTP_202_ACCEPTED)

                secret_key = settings.SECRET_KEY
                user = User.objects.filter(username= serializer.data['username']).first()
                payload = {
                    'user_id': user.id, 
                    'exp': datetime.utcnow() + timedelta(hours=1)
                }

                token = jwt.encode(key=secret_key, payload=payload, algorithm='HS256')
                
                return Response({'message':'user login sucessfull',
                                 "token":token})
            
            else:
                return Response({'message':'user not authenticated'},  status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message':"Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
        
class UserMvs(ModelViewSet):
    authentication_classes = [JwtAuthentcation]
    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names=['get', 'delete']


class ProductCb(APIView):
    authentication_classes = [JwtAuthentcation]

    def dispatch(self, request, *args, **kwargs): # any get or post request will get passed form the dispatch method

        authentication = JwtAuthentcation()
        user , _ = authentication.authenticate(request)
        print('dispatch is working')
        if user is None:
            raise AuthenticationFailed('token authentication failed')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        data = request.data
        if 'like_counts' in data:
            data.pop('like_counts')

        if not Product.objects.filter(user__id = request.user.id,  name=data['name']).exists():
            data.update({'user':request.user.id})
            serializer = ProductSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message':'product created sucessfully',
                             "data":serializer.data})
            else:
                return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
        else:
            raise serializers.ValidationError({'message':'You Have already publish this product'})
    
    def get(self , request): # user can view only other users product
        user = request.user

        others_product = Product.objects.exclude(user__id =user.id).all()
        serializer = ProductSerializer(others_product, many=True)

        return Response(serializer.data)

class ProductLike(APIView):
    authentication_classes = [JwtAuthentcation]
    def dispatch(self, request, *args, **kwargs):

        user = Dispatch.get_request(self=self, request=request)
        return super().dispatch(request, *args, **kwargs)
    
    def post(self , request):
        data = {'user': request.user.id,
                'product':request.data['id']}
        
        is_liked = Likes.objects.filter(user = request.user, product = request.data['id'])
        if is_liked.exists():
            is_liked.delete()
            product = Product.objects.filter(id = request.data['id']).first()
            product.like_counts = product.like_counts-1
            product.save()
            return Response({'message':"product disliked",} ,status=status.HTTP_204_NO_CONTENT)
        else:
            serializer = LikeSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message':"product liked",} ,status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
class AddToCart(APIView):
    authentication_classes = [JwtAuthentcation]

    def dispatch(self, request, *args, **kwargs):
        user = Dispatch.get_request(self=self, request=request)
        return super().dispatch(request, *args, **kwargs)

    def post(self , request):
        product = Product.objects.filter(id = request.data['product']).first()
        if product:
            total_price = product.price * request.data['quantity']
            data = {'user': request.user.id,
                    'product':request.data['product'],
                    'quantity':request.data['quantity'],
                    'total_price':total_price}
            serializer = AddToCartSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message':'Product added to cart', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message':'product does not exists'}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self , request):
        cart = Cart.objects.filter(user__id = request.user.id).all()
        serializer = AddToCartSerializer(cart, many=True)
        return Response(serializer.data)    
    
