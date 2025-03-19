from django.urls import path, include
from . import views


urlpatterns = [
    
    
    # Djoser urls
    path("auth/", include("djoser.urls")),  # Includes registration, login, logout, password reset, etc.
    path("auth/", include("djoser.urls.authtoken")),  # Includes JWT token endpoints
]


# # /auth/users/ (user registration)

# /auth/token/login/ (login to obtain a token)

# /auth/token/logout/