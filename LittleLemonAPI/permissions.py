from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.db.models import Q  # For OR comparison



class IsManagerOrReadOnly(BasePermission):
    """
    Custom permission to allow only managers to create menu items.
    Delivery Crew and Customer roles can only read.
    Anonymous users can also read.
    """
    
    def has_permission(self, request, view):
        
        # safe methods include GET. THey do not alter db records
        if request.method in SAFE_METHODS:
            return True  # Unauthenticated and authenticated users can GET
        
        if request.method == "POST":
            return request.user.is_authenticated and request.user.groups.filter(name="Manager").exists() #Only managers can POST
       
        return False # Deny all other HTTP method (PUT, PATCH, DELETE)
    
    
class IsManagerOrReadOnlySingleView(BasePermission):
    
    def has_permission(self, request, view):
        # Leave GET open for all 
        if request.method in SAFE_METHODS:
            return True
        
        # Only authenticated managers can access PUT, PATCH, and DELETE
        if request.method in ["PUT", "PATCH", "DELETE", 'POST'] :
            return request.user.is_authenticated and "Manager" in request.user.groups.values_list("name", flat=True)
        
        if request.method == "POST":
            return True
        
        return False # Deny all other HTTP methods (POST in this case)


# Serializer for the User group management view
class IsUserManager(BasePermission):
    def has_permission(self, request, view):
        if request.method in ["POST", "GET", "DELETE"]:
            return request.user.is_authenticated and request.user.groups.filter(name="Manager").exists()
        

class IsUserCustomer(BasePermission):
    def has_permission(self, request, view):
        if request.method in ["POST", "GET", "DELETE"]:
            return request.user.is_authenticated and not request.user.groups.filter(Q(name="Manager") | Q(name="Delivery crew")).exists()
        
        

class OrderPermissions(BasePermission):
    def has_permission(self, request, view):
        
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        
        if request.method == "POST":
            return request.user.is_authenticated and not request.user.groups.filter(Q(name="Manager") | Q(name="Delivery crew")).exists()