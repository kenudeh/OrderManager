from django.shortcuts import render
from .serliazers import *
from rest_framework.views import APIView
from rest_framework.throttling import AnonRateThrottle
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .permissions import *
import logging
from django.shortcuts import get_object_or_404

from django.db.models import Q  # For OR comparison

from django.contrib.auth.models import User, Group
from datetime import timezone



"""
MENU ITEMS ENDPOINTS
"""

# Create your views here.
class MenuItemView(APIView):
    throttle_classes = [AnonRateThrottle]
    permission_classes = [IsManagerOrReadOnly] 
    
    # For handling GET requests
    def get(self, request):
        # Retrieving all menu items for everyone (includig anonumous users)
        menu_items = MenuItem.objects.all()
        # creating a serializer instance and passing the menu items to it
        serializer = MenuItemSerializer(menu_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    # For POST requests
    def post(self,request):
        # validating incoming request
        serializer = MenuItemSerializer(data=request.data) # menu-item serializer instance
        if not serializer.is_valid():
            return Response(
                {
                    "status": "error",
                    "message": "Invalid input",
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
            
        # Save the data
        try:
            serializer.save()
            return Response(
                {
                    "status": "success",
                    "message": "Request submited successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            # Using Django's logging framework to log the error for debugging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to save data: {str(e)}")
            
            return Response(
                {
                    "status": "error",
                    "message": "Failed to save data",
                    "errors": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
         
            
    def put(self, request):
        return Response({"detail": "Method Not Allowed"}, status=status.HTTP_403_FORBIDDEN)
         
            
    def patch(self, request):
        return Response({"detail": "Method Not Allowed"}, status=status.HTTP_403_FORBIDDEN)
         
            
    def delete(self, request):
        return Response({"detail": "Method Not Allowed"}, status=status.HTTP_403_FORBIDDEN)
    
    
    
    
class SingleMenuItem(APIView):
    permission_classes = [IsManagerOrReadOnlySingleView]
    throttle_classes = [AnonRateThrottle]
    
    # Method to fetch a single MenuItem object by its primary key
    def get(self, request, pk):
        # retrieve the menu item by its primary key or return an error
        menu_items = get_object_or_404(MenuItem, pk=pk)
        serializer = MenuItemSerializer(menu_items)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def put(self,request, pk):
        # Retrieving a menu item using its primary key
        menu_item = get_object_or_404(MenuItem, pk=pk)
        
        # Binding the existing menu item with the new data from the request
        serializer = MenuItemSerializer(menu_item, data=request.data)
        
        # Validating the data using the serializer and saving the data to the db, if true
        if serializer.is_valid():
            serializer.save()
            # Returning the updated data
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Return an error if serializer validation fails
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    def patch(self,request, pk):
        # Retrieving a menu item using its primary key
        menu_item = get_object_or_404(MenuItem, pk=pk)
        
        # Deserialize request data and update the provided field alone. Setting partial=True ensures only modified fields are updated 
        serializer = MenuItemSerializer(menu_item, data=request.data, partial=True)
        
        # Validating the data using the serializer and saving the data to the db, if true
        if serializer.is_valid():
            serializer.save()
            # Returning the updated data
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Return an error if serializer validation fails
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    # Method to remove a menu item specified by 'pk' in the request
    def delete(self,request, pk):
        # REtrieve the menu item that matches the supplied primary key, or return a 404 error if not found
        menu_item = get_object_or_404(MenuItem, pk=pk)
        
        # Delete the retrieved item from the db
        menu_item.delete()
        
        # Return a success message
        return Response({"detail": "Item deleted successfully"}, status=status.HTTP_200_OK)
    
    
    
    def post(self,request, pk):
        return Response({"detail": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    


"""
USER GROUP MANAGEMENT ENDPOINTS
"""
    
# Endpoint for viewing and assigning users to the managers group 
class ManagersGroupView(APIView):
    permission_classes = [IsUserManager]
    throttle_classes = [AnonRateThrottle]
    
    # Returns all users in the "Manager" group
    def get(self, request):
        managers = User.objects.filter(groups__name="Manager")
        serializer = UserSerializer(managers, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    # Adds a user to the Managers group. Requires a "username" or "userid" payload
    def post(self,request):
        # Obtaining the user from the payload - can be either of username or user ID
        user_id = request.data.get("user_id")
        username = request.data.get("username")
        
        # Checking the payload for userID or username
        if not user_id and not username:
            return Response({"error": "Provide a user_id or username"}, status=status.HTTP_400_BAD_REQUEST)
        
        # fetching the user instance by ID or username
        try:
            if user_id:
                user = User.objects.get(id=user_id)
            else:
                user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "User not found!"}, status=status.HTTP_404_NOT_FOUND)
        
            
        # Obtaining the manager group (or creating one if it does not exist). I used get_or_create to avoid error that arrises with using get()
        manager_group, _ = Group.objects.get_or_create(name="Manager")  # Ignored the Boolean part of get_or_create's response with the underscore. 
        
        # Checking if the managers group already contains the user and returning an error if true
        if manager_group.user_set.filter(Q(id=user.id) | Q(username=user.username)).exists():  # This logic can also be used to fetch the user instance by ID or username 
            return Response ({"error": "user already belongs to this group"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Adding the user to the group
        user.groups.add(manager_group)
        
        return Response(
            {"message": "user added to the Manager group"}, status=status.HTTP_201_CREATED
        )
        
        

# Endpoint for removing a manager
class RemoveFromManagersView(APIView):
        permission_classes = [IsUserManager]
        throttle_classes = [AnonRateThrottle]
        
        def delete(self, request, pk):
            # fetching the user instance by ID
            try:
                user = User.objects.get(id=pk)
            except User.DoesNotExist:
                return Response({"error": "User not found!"}, status=status.HTTP_404_NOT_FOUND)
                
            # Obtaining the manager group (or creating one if it does not exist)
            manager_group, _ = Group.objects.get_or_create(name="Manager")  # Ignored the Boolean part of get_or_create's response with the underscore
            
            # Checking if user exists already in the Managers group and returning an error if true
            if not user.groups.filter(name="Manager").exists():  # This logic can also be used to fetch the user instance by ID or username 
                return Response ({"error": "User is not a manager"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Removing the user from the group
            user.groups.remove(manager_group)
            
            return Response(
                {"message": "User removed from the Manager group"}, status=status.HTTP_200_OK
            )
            


class DeliveryCrewView(APIView):
    permission_classes = [IsUserManager]
    throttle_classes = [AnonRateThrottle]

    
    def get(self, request):
        delivery_crew = User.objects.filter(groups__name = "Delivery crew")
        serializer = UserSerializer(delivery_crew, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    # Method to add a user to the Delivery Crew group
    def post(self, request):
        # Obtaining the user from the payload - can be either of username or user ID
        username = request.data.get("username")
        user_id = request.data.get("user_id")
        
        # Checking the payload for username or userID
        if not username and not user_id:
            return Response({"error": "Provide a user_id or username" }, status=status.HTTP_400_BAD_REQUEST)
        
        # fetching the user instance by ID or username
        try:
            if user_id:
                user = User.objects.get(id=user_id)
            else:
                user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "User not found!"}, status=status.HTTP_404_NOT_FOUND)
        
                
        # Obtaining the delivery crew group (or creating one if it does not exist). Used get_or_create to avoid errors that arrises with using get()
        delivery_group, _ = Group.objects.get_or_create(name="Delivery crew")  # Ignored the Boolean part of get_or_create's response with the underscore. 
        
        # Checking if user exists already in the Delivery crew group and returning an error if true
        if delivery_group.user_set.filter( Q(id=user.id) | Q(username=user.username) ).exists():
            return Response ({"error": "user already belongs to this group"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Adding the user to the group
        user.groups.add(delivery_group)
        
        return Response(
            {"message": "user added to the Delivery crew"}, status=status.HTTP_201_CREATED
        )
        
        
class RemoveFromDeliveryCrew(APIView):
    permission_classes = [IsUserManager]
    throttle_classes = [AnonRateThrottle]
    
    def delete(self, request, pk):
        # fetching the user instance by the primary key provided in the URL
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        # Obtaining the delivery crew group or creating one if it doesn't exist
        delivery_group, _ = Group.objects.get_or_create(name="Delivery crew")
        
        # Checking if user exists already in the delivery crew group and returning an error if true
        if not user.groups.filter(name="Delivery crew").exists():
            return Response ({"error": "User is not a delivery crew memeber"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Removing the user from the group
        user.groups.remove(delivery_group)
        
        return Response(
                {"message": "User removed from the delivery crew"}, status=status.HTTP_200_OK
            )
        
        
        
    
"""
CART MANAGEMENT ENDPOINTS
"""
class CartView(APIView):
    permission_classes = [IsUserCustomer]
    throttle_classes = [AnonRateThrottle]

    def get(self, request, *args, **kwargs):
        # Filtering the cart model by the current user
        cart_items = Cart.objects.filter(user=request.user)
        # Serializing the queryset and returning the data
        serializer = CartSerializer(cart_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    
    
    def post(self, request, *arg, **kwargs):
        # Obtaining the menu item or returning a 404 otherwise
        menuitem = get_object_or_404(MenuItem, id=request.data.get('item_id'))

        # Chaecking if currrently authenticated user already has item in cart
        if Cart.objects.filter(user=request.user, menuitem=menuitem).exists():
            return Response(
                {"error": "This item is already in your cart"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Calculating the price
        quantity = int(request.data.get('quantity', 1))
        unit_price = menuitem.price
        price = quantity * unit_price
        
        # Then, creating a cart item instance
        cart_item = Cart.objects.create(
            user = request.user,
            menuitem = menuitem,
            quantity = quantity,
            unit_price = unit_price,
            price = price
        )
        
        serializer = CartSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
    def delete(self, request, *args, **kwargs):
        
        if not Cart.objects.filter(user=request.user).exists():
            return Response (
                {"message": "No items in your cart"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        Cart.objects.filter(user=request.user).delete()
        return Response({"message": "Cart items deleted successfully"},status=status.HTTP_200_OK)
        
        
    
"""
ORDER MANAGEMENT ENDPOINTS
"""
# Converts cart ites to an order
class OrdersView(APIView):
    permission_classes = [OrderPermissions]
    throttle_classes = [AnonRateThrottle]
    
    def get(self, request):
        return Response({"detail": "Request going through"})
    
    
    def post(self,request):
        user = request.user
        
        # Get cart items directly from the CartView view
        cart_items = Cart.objects.filter(user=request.user).values(
            'menuitem_id',  
            'quantity',
            'unit_price',
            'price'
        )    
        
        if not cart_items:
            return Response(
                {"detail": "Your cart is empty."},
                status=status.HTTP_400_BAD_REQUEST
            )

        
        # Create the order 
        order_total = sum(item['price'] for item in cart_items)
        order = Order.objects.create(
            user=user,
            status=False,
            total=order_total,
            date=timezone.now()
        )
        
        
        # Create order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                menuitem_id=item['menuitem_id'],  # Matches your FK name
                quantity=item['quantity'],
                unit_price=item['unit_price'],
                price=item['price']
            )
            
        # Clear the cart
        Cart.objects.filter(user=user).delete()

        return Response(
            {"detail": "Order created successfully", "order_id": order.id},
            status=status.HTTP_201_CREATED
        )