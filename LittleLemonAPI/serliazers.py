from .models import *
from rest_framework import serializers
from django.contrib.auth.models import Group



class MenuItemSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        read_only = True,
        slug_field = 'title'
    )
    
    class Meta:
        fields = '__all__'
        model = MenuItem
        read_only_fields = ('featured', 'id')
        


# Group serializer to be used as a nested serializer in UserSerializer
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']
           
        
class UserSerializer (serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True) #to be used in representing the 'groups' field
    
    class Meta:
        model = User
        fields = ['id', "username", "first_name", "last_name", "email", "groups", "date_joined" ]
        
        
class CartSerializer(serializers.ModelSerializer):
    menuitem = serializers.SlugRelatedField(
        read_only = True,
        slug_field = 'title'
    )
    
    user = serializers.SlugRelatedField(
        read_only = True,
        slug_field = 'username'
    )
    
    class Meta:
        model = Cart
        fields = ["user", "menuitem", 'quantity', "unit_price", "price",  ]   



class OrderSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Order
        fields = "__all__"