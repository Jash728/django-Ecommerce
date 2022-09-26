from contextlib import nullcontext
from distutils.command.upload import upload
import profile
from tkinter import ACTIVE
from tokenize import blank_re
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid
import datetime

User._meta.get_field('email')._unique = True

STATE_CHOICES = (
    ('Gujarat', 'Gujarat'),
    ('Rajasthan', 'Rajasthan'),
    ('Maharashtra', 'Maharashtra'),
    ('Delhi', 'Delhi'),
)

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=50)

    def __str__(self):
        return str(self.id)


	

class Brand(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return str(self.id)


class Product(models.Model):
    title = models.CharField(max_length = 200)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description  = models.TextField()
    brand = models.ForeignKey('Brand', null=True, on_delete = models.CASCADE)
    category  = models.ForeignKey('Category',  null=True, on_delete = models.CASCADE)
    is_dashboard  = models.BooleanField(default=0)
    product_img = models.ImageField(upload_to = 'productimg')


    def __str__(self):
        return str(self.id)

class Coupon(models.Model):
    code = models.CharField(max_length=15)
    is_expired = models.BooleanField(default = False)
    discount = models.IntegerField(default=100)
    minimum_amount = models.IntegerField(default=500)

    def __str__(self):
        return str(self.id)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity =   models.PositiveIntegerField(default=1)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank = True) 
    

    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity*self.product.discounted_price



class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank = True) 
   
    @property
    def total_cost(self):
        return self.quantity*self.product.discounted_price

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete = models.CASCADE)
    profession = models.TextField(blank=True,null=True)
    bio = models.TextField()
    profile_pic = models.ImageField(null=True, upload_to = "images/profile/")

    def __str__(self):
        return str(self.user)

class Category(models.Model):
    name = models.CharField(max_length=200)
    pid = models.IntegerField()
    status = models.IntegerField()
    description  = models.TextField()
    is_dashboard = models.BooleanField(default=0)
   
    
    def __str__(self):
        return str(self.id)

class Slider(models.Model):
    name = models.CharField(max_length = 200)
    description = models.TextField()
    slider_image = models.ImageField(null=True, upload_to = "sliderimg")
    type = models.CharField(max_length=200)

    def __str__(self):
        return str(self.id)



# class Coupon(models.Model):
#     code = models.CharField(max_length=50)
#     valid_from = models.DateTimeField(default = None)
#     valid_to = models.DateTimeField(default = None)
#     discount_price = models.IntegerField(default=100)
#     active = models.BooleanField(default=False)

#     def __str__(self):
#         return self.code
