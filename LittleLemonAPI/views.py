from django.shortcuts import render
from .serliazers import *
from rest_framework.views import APIView
from rest_framework.throttling import AnonRateThrottle
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .permissions import *
import logging
from django.shortcuts import get_object_or_404

from django.db.models import Q  # For OR comparison




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
    
    
    
    def POST(self,request, pk):
        return Response({"detail": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    
# Endpoint for viewing and assigning users to the managers group 
class GroupManagementView(APIView):
    permission_classes = [IsUserManager]
    throttle_classes = [AnonRateThrottle]
    
    def get(self, request):
        managers = User.objects.filter(groups__name="Manager")
        serializer = UserSerializer(managers, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
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
            
        # Obtaining the manager group (or creating one if it does not exist)
        manager_group, _ = Group.objects.get_or_create(name="Manager")  # Ignored the Boolean part of get_or_create's response with the underscore
        
        # Checking if user exists already in the Managers group and returning an error if true
        if manager_group.user_set.filter(Q(id=user.id) | Q(username=user.username)).exists():  # This logic can also be used to fetch the user instance by ID or username 
            return Response ({"error": "user already a belongs to this group"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Adding the user to the group
        user.groups.add(manager_group)
        
        return Response(
            {"message": "user added to the Manager group"}, status=status.HTTP_201_CREATED
        )
        
    
    class GroupManagementSingleView(APIView):
        permission_classes = [IsUserManager]
        throttle_classes = [AnonRateThrottle]
        
            