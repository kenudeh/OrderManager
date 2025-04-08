from django.contrib import admin
from .models import *

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
admin.site.register(Category, CategoryAdmin)


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'category')
admin.site.register(MenuItem, MenuItemAdmin)


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'menuitem', 'quantity')
admin.site.register(Cart, CartAdmin)


class OrderAdmin(admin.ModelAdmin):
    def get_fields(self, request, obj=None):
        # Delivery crew sees ONLY these fields (simpler UI)
        if request.user.groups.filter(name='Delivery crew').exists():
            return ['status']  # Whitelist
        
        if request.user.groups.filter(name='Manager').exists():
            return ['delivery_crew']
        
        # Superusers/other groups see all fields
        return super().get_fields(request, obj)

admin.site.register(Order, OrderAdmin)



class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'menuitem', 'quantity', 'price')
admin.site.register(OrderItem, OrderItemAdmin)


