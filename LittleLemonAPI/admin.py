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
    list_display = ('user', 'delivery_crew', 'status', 'total')
admin.site.register(Order, OrderAdmin)



class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'menuitem', 'quantity', 'price')
admin.site.register(OrderItem, OrderItemAdmin)


