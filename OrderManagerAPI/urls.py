from django.urls import path, include
from . import views


urlpatterns = [
    path('menu-items', views.MenuItemView.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuItem.as_view()),
    path('groups/manager/users', views.ManagersGroupView.as_view()),
    path('groups/manager/users/<int:pk>', views.RemoveFromManagersView.as_view()),
    path('groups/delivery-crew/users', views.DeliveryCrewView.as_view()),
    path('groups/delivery-crew/users/<int:pk>', views.RemoveFromDeliveryCrew.as_view()),
    path('cart/menu-items', views.CartView.as_view()),
    path('orders', views.OrdersView.as_view()),
    path('orders/<int:pk>', views.OrderDetailView.as_view()),
    path('categories', views.CategoryListView.as_view()),
    path('categories/<int:category_id>/items', views.CategoryMenuItemsView.as_view()),
    # Djoser urls
    path("auth/", include("djoser.urls")),  # Includes registration, login, logout, password reset, etc.
    path("auth/", include("djoser.urls.authtoken")),  # Includes  token endpoints
]


# api/auth/users/ (user registration)
# api/auth/users/me (display currently authenticated user)
# api/auth/token/login (Generates access token. Username and password must be included in the request)
# /token/logout/