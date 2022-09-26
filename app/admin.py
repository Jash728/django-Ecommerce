from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import (Customer, Brand, Product, Cart, OrderPlaced, Profile, Category, Slider, Coupon)

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'locality', 'city', 'zipcode', 'state']

@admin.register(Brand)
class BrandModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'selling_price', 'discounted_price', 'description', 'brand', 'category', 'is_dashboard', 'product_img']

# Register your models here.
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity', 'coupon']


@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer', 'product', 'quantity', 'ordered_date', 'coupon']

admin.site.register(Profile)

@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'pid', 'status', 'description', 'is_dashboard']

@admin.register(Slider)
class SliderModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'slider_image' , 'type']

@admin.register(Coupon)
class CouponModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'is_expired', 'discount', 'minimum_amount']

