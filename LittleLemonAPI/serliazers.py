from .models import *
from rest_framework import serializers



class MenuItemSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        read_only = True,
        slug_field = 'title'
    )
    
    
    class Meta:
        fields = '__all__'
        model = MenuItem
        