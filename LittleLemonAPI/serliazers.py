from .models import *
from rest_framework import serializers



class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = MenuItem
        