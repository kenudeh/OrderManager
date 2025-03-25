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


class OrderItemSerializer(serializers.ModelSerializer):
    menuitem_name = serializers.CharField(source='menuitem.title', read_only = True) 
    
    class Meta:
        model = OrderItem
        fields = ['menuitem', 'menuitem_name', 'quantity', 'unit_price', 'price']



class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(source='orderitem_set', many = True)
    username = serializers.CharField(source='user.username', read_only=True)
    delivery_crew_name = serializers.SerializerMethodField()
    
    class Meta: 
        model = Order
        fields = [
           'id', 'user', 'username', 
            'delivery_crew', 'delivery_crew_name',
            'status', 'total', 'date', 'items'
        ]
        
    def get_delivery_crew_name(self, obj):
        # Only show delivery crew name if user is staff/manager
        request = self.context.get('request')
        if request and (request.user.groups.filter(name='Manager').exists() or request.user.groups.filter(name='Delivery crew').exists()):
            return obj.delivery_crew.username if obj.delivery_crew else None
        return None # Hidden for customers
    
    
    def to_representation(self, instance):
        # Remove delivery_crew field for customers
        data = super().to_representation(instance)
        request = self.context.get('request')
        if request and not (request.user.groups.filter(name='Manager').exists() or request.user.groups.filter(name='Delivery crew').exists()):
            data.pop('delivery_crew', None)
            data.pop('delivery_crew_name', None)
        return data
    
    
class SingleOrderViewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = [
           'id', 'user', 'username', 
            'delivery_crew', 'delivery_crew_name',
            'status', 'total', 'date', 'items'
        ]