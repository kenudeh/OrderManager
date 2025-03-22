from django.shortcuts import render
from .serliazers import *
from rest_framework.views import APIView
from rest_framework.throttling import AnonRateThrottle
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsManagerOrReadOnly
import logging




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
    
    
