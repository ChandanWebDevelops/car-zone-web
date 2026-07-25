from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Brand, Car, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'country_of_origin']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['image_tag', 'model_name', 'brand', 'category', 'year', 'price', 'stock', 'is_available']
    list_filter = ['is_available', 'brand', 'category', 'year', 'transmission', 'fuel_type']
    search_fields = ['model_name', 'brand__name', 'description']
    prepopulated_fields = {'slug': ('model_name',)}
    list_editable = ['stock', 'is_available']

    @admin.display(description='Image')
    def image_tag(self, obj):
        if obj.image:
            # Correct usage: The string with {} is the 1st arg, the variable is the 2nd arg
            return format_html('<img src="{}" style="max-width:50px; max-height:50px; border-radius:5px;" />', obj.image.url)
        return "-"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'paid', 'created_at', 'updated_at']
    list_filter = ['paid', 'created_at', 'updated_at']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'car', 'price', 'quantity']