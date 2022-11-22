from django.db import models

# Create your models here.

from ctypes import addressof
from email.policy import default
from pyexpat import model
from django.db import models

# Create your models here.
class Users(models.Model):
    
    email = models.CharField(max_length=50)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    phone = models.CharField(max_length=10)
    status = models.BooleanField(default=True)

class add_category(models.Model):
    category_name = models.CharField(max_length=20)

class category_by_price(models.Model):
    memory=models.CharField(max_length=50)
    cat_id=models.ForeignKey(add_category,on_delete=models.CASCADE)
    image1=models.ImageField(upload_to='media',blank=True)

class product(models.Model):
    product_id=models.CharField(max_length=6)
    product_name=models.CharField(max_length=50)
    p_description=models.CharField(max_length=200)
    actual_price=models.IntegerField(default=True)
    actual_price_category=models.IntegerField(default=True)
    price=models.IntegerField()
    stock=models.IntegerField(default=True)
    ram=models.CharField(max_length=6,default=True)
    storage=models.CharField(max_length=6,default=True)
    cat_id=models.ForeignKey(add_category,on_delete=models.CASCADE,related_name="add_category_table")
    image1=models.ImageField(upload_to='media',blank=True)
    image2=models.ImageField(upload_to='media',blank=True)
    image3=models.ImageField(upload_to='media',blank=True)
    image4=models.ImageField(upload_to='media',blank=True)
    # iOS 15.4, upgradable to iOS 16.0.2, Apple A15 Bionic (5 nm) Hexa-core (2x3.22 GHz + 4x1.82 GHz) Apple GPU (4-core graphics)

class Cart(models.Model):
    user_id=models.ForeignKey(Users,on_delete=models.CASCADE,related_name="Users_table")
    product_id=models.ForeignKey(product,on_delete=models.CASCADE,related_name="product_table")
    quantity=models.CharField(max_length=5)

class Address(models.Model):
    user_id=models.IntegerField()
    buyer_name=models.CharField(max_length=50)
    buyer_phone=models.CharField(max_length=11)
    address=models.CharField(max_length=100)
    pincode=models.CharField(max_length=7)
    city=models.CharField(max_length=50)
    state=models.CharField(max_length=30)
    country=models.CharField(max_length=50)

class Payment(models.Model):
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    STATUS = (
        ('New','New'),
        ('Confirmed','Confirmed'),
        ('Shipped','Shipped'),
        ('Out of delivery','Out of delivery'),
        ('Cancelled','Cancelled'),
        ('Returned','Returned')
    )
    user = models.ForeignKey(Users, on_delete=models.SET_NULL,null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL,null=True,blank=True)
    address = models.ForeignKey(Address,on_delete=models.CASCADE)
    order_number = models.CharField(max_length=20)
    order_total = models.FloatField()
    status = models.CharField(max_length=50,choices=STATUS,default='Confirmed')
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class OrderProduct(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL,null=True,blank=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    product = models.ForeignKey(product,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50,default='Confirmed')
    out_for_delivery = models.DateTimeField(blank=True,null=True)

class Wishlist(models.Model):
    user_table=models.ForeignKey(Users,on_delete=models.CASCADE)
    product_table=models.ForeignKey(product,on_delete=models.CASCADE)

class Coupan(models.Model):
    coupan_code=models.CharField(max_length=25)
    start_date_and_time=models.DateTimeField()
    end_date_and_time=models.DateTimeField()
    discount_amount=models.CharField(max_length=5,blank=True)
    discount_percentage=models.CharField(max_length=5,blank=True)
    maximum_usage=models.IntegerField(blank=True)

class Coupan_applied(models.Model):
    coupan=models.IntegerField()
    user=models.IntegerField()

class Category_offer(models.Model):
    Category=models.ForeignKey(add_category,on_delete=models.CASCADE)
    start_date_and_time=models.DateField()
    end_date_and_time=models.DateField()
    discount_amount=models.CharField(max_length=5,blank=True)
    discount_percentage=models.CharField(max_length=5,blank=True)







class Product_offer(models.Model):
    product=models.ForeignKey(product,on_delete=models.CASCADE)
    start_date_and_time=models.DateField()
    end_date_and_time=models.DateField()
    discount_amount=models.CharField(max_length=5,blank=True)
    discount_percentage= models.CharField(max_length=5,blank=True)



class CartGuestUser(models.Model):
    user_session=models.CharField(max_length=20)
    pid=models.ForeignKey(product,on_delete=models.CASCADE)
    qty=models.CharField(max_length=5)


class sales_report(models.Model):
    date = models.DateField(null=True)
    product_name = models.CharField(null=True,max_length=100)
    quantity = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)


class monthly_sales_report(models.Model):
    date = models.DateField(null=True)
    product_name = models.CharField(null=True, max_length=100)
    quantity = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)


class SalesReport(models.Model):
    productName = models.CharField(max_length=100)
    categoryName = models.CharField(max_length=100)
    date = models.DateField()
    quantity = models.IntegerField()
    productPrice = models.FloatField()    