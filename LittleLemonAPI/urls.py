from django.urls import path, include
from . import views


urlpatterns = [
    path('menu-item', views.MenuItemView.as_view()),
    path('menu-item/<int:pk>', views.SingleMenuItem.as_view()),
    
    # Djoser urls
    path("", include("djoser.urls")),  # Includes registration, login, logout, password reset, etc.
    path("", include("djoser.urls.authtoken")),  # Includes  token endpoints
]


# api/users/ (user registration)
# api/users/me (display currently authenticated user)
# api/token/login (Generates access token. Username and password must be included in the request)
# /token/logout/