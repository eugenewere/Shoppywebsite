import datetime

from django.contrib.auth import get_user_model
from django.db import models

# from .models import *

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False, blank=False )
    parent_id = models.ForeignKey('Category',  on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % (self.name)


class Brand(models.Model):
    name = models.CharField(max_length=50)
    # parent= models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s (%s)' % (self.name,  (self.category.name))


class Seller(get_user_model()):
    # first_name = models.CharField(max_length=100, null=False, blank= False)
    # last_name = models.CharField(max_length=100, null=False, blank= False)
    phone_number = models.CharField(max_length=20, null=False, blank= False)
    # email = models.EmailField(max_length=100, unique=True, null=False, blank=False)
    # password = models.CharField(max_length=200)
    business_no = models.CharField(max_length=100,null=False, unique=True, blank=False)
    store_logo= models.ImageField(default="nologo.jpg", upload_to='store_logo', max_length=200, null=True) #height_field=None, width_field=None
    store_name = models.CharField(max_length=100, null=False, unique=True)
    # VERIFIED=1
    # UNVERIFIED=2

    # SELLER_STATUS = (
    #     (VERIFIED, 'Verified'),
    #     (UNVERIFIED, 'Unverified'),
    # )
    # status = models.IntegerField(choices=SELLER_STATUS, max_length=100, default=VERIFIED)

    SELLER_STATUS=(
        ('VERIFIED','Verified'),
        ('UNVERIFIED','Unverified'),
    )
    status= models.CharField(choices=SELLER_STATUS, max_length=100, default='Unverified')
    country = models.CharField(max_length=100, null=False)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = 'Seller'
        verbose_name_plural = 'Sellers'

    def __str__(self):
        return '%s %s (%s)' % (self.first_name, self.last_name, (self.store_name))


class Product(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    unit_cost=models.FloatField(max_length=50)
    product_brand = models.ForeignKey(Brand, on_delete=models.DO_NOTHING)
    short_description= models.TextField()
    long_description= models.TextField()
    featured_url= models.ImageField(default="no_product_img.jpg", upload_to="product_images", max_length=200) #height_field=None, width_field=None

    PRODUCT_STATUS=(
        ('FEATURED','Featured'),
        ('NORMAL','Normal'),
    )
    status=models.CharField(choices=PRODUCT_STATUS, default='Normal', max_length=200)

    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


    def __str__(self):
        return '%s (%s)' % (self.name,(self.seller))

class Buyer(get_user_model()):
    # first_name = models.CharField(max_length=100, null=False, blank=False)
    # last_name = models.CharField(max_length=100, null=False, blank=False)
    phone_number = models.CharField(max_length=20,null=False, blank=False)
    # email = models.EmailField(max_length=100, unique=True, null=False)
    # password = models.CharField(max_length=200)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s %s'% (self.first_name, self.last_name)

    class Meta:
        verbose_name = 'Buyer'
        verbose_name_plural = 'Buyers'
# get_user_model()



class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField( default="", upload_to='images', height_field=None, width_field=None, max_length=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s (%s)' % (self.image,(self.product.name))


# class Brand(models.Model):
#     name = models.CharField(max_length=50)
#     parent= models.ForeignKey(Product, on_delete=models.CASCADE)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return '%s (%s)' % (self.name,  (self.category.name))


class Review(models.Model):
    buyer= models.ForeignKey(Buyer, on_delete=models.CASCADE)
    comments= models.TextField(max_length=100)
    ratings= models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):        
        return '%s (%s)' % (self.comments, (self.ratings))


class Wishlist(models.Model):
    product= models.ForeignKey(Product, on_delete=models.CASCADE)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Region(models.Model):
    name=models.CharField(max_length=50, null=False)
    region_cost = models.FloatField( null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s (%s)' % (self.name,( self.region_cost))

# we have no string being returned foe wishlist
class Checkout(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    region=models.ForeignKey(Region, on_delete=models.CASCADE)
    phonenumber = models.CharField(max_length=20, null=False)
    city = models.CharField(max_length=20, null=False)
    reference_code = models.CharField(max_length=10 )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    CHECKOUT_STATUS=(
        ('VERIFIED','verified'),
        ('UNVERIFIED','unverified'),
    )
    status= models.CharField(choices=CHECKOUT_STATUS, max_length=100, default='Unverified')

    class Meta:
        verbose_name = 'Checkout'
        verbose_name_plural = 'Checkouts'

    def __str__(self):
        return '%s (%s)' % (self.buyer.name, (self.city))

class Order_Product(models.Model):
    product= models.ForeignKey(Product, on_delete=models.CASCADE)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE)
    quantity =  models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   
    def __str__(self):        
        return '%s %s(%s)' % (self.buyer.name, self.product.name, (self.quantity))



#check on status
class Payment(models.Model):
    checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE)
    payment_method = models.CharField( max_length=50)
    amount = models.FloatField()
    reference_code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    PAYMENT=(
        ('VERIFIED','verified'),
        ('UNVERIFIED','unverified'),
    )
    status= models.CharField(choices=PAYMENT,max_length=100, default='Unverified')

class Order_Delivery(models.Model):
    checkout= models.ForeignKey(Checkout,  on_delete=models.CASCADE)
    payment=models.ForeignKey(Payment, on_delete=models.CASCADE)
    delivery_status =models.CharField(max_length=50)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   
    def __str__(self):        
        return '%s' % (self.delivery_status)

#can this offer return an product image alongside the offer
class Offer(models.Model):  #
    offer =models.CharField(max_length=50)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    discount =models.IntegerField(null=True)
    duration=models.DateTimeField(default=datetime.datetime.now())     #  auto_now_add=True
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):        
            return '%s %s' % (self.product.name, self.offer)

class Carousel(models.Model):
    image = models.ImageField(default="", upload_to='couresel', null=True) #height_field=None, width_field=None,
    description = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):        
        return '%s %s ' % (self.image, self.description)


class Inventory(models.Model):
    product= models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):        
        return '%s %s' % (self.product.name, (self.quantity))


class Variant(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):        
        return '%s' % (self.name)

class Variant_Option(models.Model):
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):        
        return '%s (%s)' % (self.variant.name, (self.name))


class Product_Variant(models.Model):
    product= models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):        
        return '%s (%s)' % (self.product.name, (self.variant))

# #check on status
# class Payment(models.Model):
#     checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE)
#     payment_method = models.CharField( max_length=50)
#     amount = models.FloatField()
#     reference_code = models.CharField(max_length=10)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     VERIFIED=1
#     UNVERIFIED=2
#
#     PAYMENT=(
#         (VERIFIED,'verified'),
#         (UNVERIFIED,'unverified'),
#     )
#     status= models.CharField(choices=PAYMENT,max_length=100, default= UNVERIFIED)

   




