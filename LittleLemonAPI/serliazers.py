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
        
        
class UserSerializer (serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
        