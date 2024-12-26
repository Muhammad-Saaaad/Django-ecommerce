from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import *

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        if not 'username' in data:
            raise serializers.ValidationError("username not given")
        else:
            if User.objects.filter(username=data['username']).exists():
                raise serializers.ValidationError("Username already taken")
        if not 'password' in data:
            raise serializers.ValidationError("Password not given")
        
        print("_______________________________________",data)

        return data
    
    def create(self, validated_data):
        # print(validated_data)
        user = User.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return validated_data
            

class LoginSerializer(serializers.Serializer):
    username= serializers.CharField()
    password= serializers.CharField()
    
class UserSerializer(serializers.ModelSerializer):

    class Meta: 
        model = get_user_model()
        fields = ['id', 'username', 'password', 'is_superuser', 'is_active', 'is_staff']

class ProductSerializer(serializers.ModelSerializer):

    # user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = Product
        fields= '__all__'

    # def create(self, validated_data):
    #     # user = validated_data.pop('user') # as here the user is the user object
    #     if 'like_counts' in validated_data:
    #         validated_data.pop('like_counts')
    #     # get_user = User.objects.get(id = user.id
    #     if not Product.objects.filter(user__id = validated_data['user'], name=validated_data['name']).exists():
    #         product = Product.objects.create(**validated_data)
    #         return product
    #     else:
    #         raise serializers.ValidationError({'message':'You Have already publish this product'})

# class Product_view(serializers.ModelSerializer): # do this when you want to encode the token with any value

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = '__all__'

    def validate(self, data):

        if User.objects.filter(id = data['user'].id).exists() and Product.objects.filter(id = data['product'].id).exists():
            product = Product.objects.filter(id = data['product'].id).first()
            product.like_counts = product.like_counts+1
            product.save()
            return data
        else:
            raise ValueError('user id or product id is not valid')

class AddToCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = '__all__'