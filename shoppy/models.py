
from django.contrib.auth import get_user_model
from django.db import models
from datetime import datetime
import datetime
from datetime import timedelta
# from .models import *
from django.db.models import Sum


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False, blank=False )
    parent_id = models.ForeignKey('Category',  on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % (self.name)

    @property
    def has_children(self):
        if Category.objects.filter(parent_id=self).count() > 0:
            return True
        else:
            return False

    @property
    def children(self):
        return Category.objects.filter(parent_id=self)[:6]



    @property
    def is_child(self):
        if self.parent_id:
            return True
        else:
            return False

    def childern_count(self):
        category_childern=Category.objects.filter(parent_id=self).count()
        if category_childern:
            return category_childern
        else:
            return category_childern

class Brand(models.Model):
    name = models.CharField(max_length=50)
    # parent= models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='brands', on_delete=models.CASCADE)
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
    store_logo= models.ImageField(default="no_seller_logo.jpg", upload_to='store_logo', max_length=200, null=True) #height_field=None, width_field=None
    store_name = models.CharField(max_length=100, null=False, unique=True)

    SELLER_STATUS=(
        ('VERIFIED','Verified'),
        ('UNVERIFIED','Unverified'),
    )
    status= models.CharField(choices=SELLER_STATUS, max_length=100, default='UNVERIFIED')
    country = models.CharField(max_length=100, null=False)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = 'Seller'
        verbose_name_plural = 'Sellers'

    def __str__(self):
        return '%s %s (%s)' % (self.first_name, self.last_name, (self.store_name))



    @property
    def order_products(self):
        product=Product.objects.filter(seller=self)
        orderproducts = Order_Product.objects.filter(product=product)
        return orderproducts


    def ordered_products(self, product_id):
        product = Product.objects.filter(id=product_id)
        if product is None:
            return False
        order = self.order_products
        if order.filter(checkout__isnull=False):
            return True
        return False






class Product(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    unit_cost=models.FloatField(max_length=50)
    product_brand = models.ForeignKey(Brand, related_name='products', on_delete=models.DO_NOTHING)
    short_description= models.TextField()
    long_description= models.TextField()
    featured_url= models.ImageField(default="no_product_img.jpg", upload_to="product_images", max_length=200) #height_field=None, width_field=None

    PRODUCT_STATUS=(
        ('FEATURED','Featured'),
        ('NORMAL','Normal'),
    )
    status=models.CharField(choices=PRODUCT_STATUS, default='NORMAL', max_length=200)

    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


    def __str__(self):
        return '%s (%s)' % (self.name,(self.seller))



    @property
    def images(self):
        return Image.objects.filter(product=self)

    @property
    def product_variant_options(self):
        return Product_Variant_Options.objects.filter(product=self)

    def variants(self):
        variants = []
        for product_variant_option in self.product_variant_options:
            variants.append(product_variant_option.variant_options.variant)
        return variants

    @property
    def inventory_qty(self):
        inventory=Inventory.objects.filter(product=self).first()
        if inventory is not None:
            inventoryqty=inventory.quantity
            # print(inventory.discount)
            return inventoryqty
        else:
            return 0

    @property
    def price_after_offer(self):
        product = Product.objects.filter(id=self.id).first()
        offer=Offer.objects.filter(product=product).first()
        if offer is not None:
            discount=offer.discount
            offer_cost = (100-float(discount))/100 * float(product.unit_cost)
            # print(offer_cost)
            return float(offer_cost)
        else:
            return product.unit_cost

    # @property
    # def offer_time(self):
    #     print(self)
    #     product = Product.objects.filter(id=self.id).first()
    #     offer = Offer.objects.filter(product=product)
    #     print(offer)
    #     if offer is not None:
    #         print('offer found')
    #         print(offer.start_time)
    #         # print(offer.end_time)
    #         date_format = '%Y-%m-%d'
    #         a = datetime.datetime.strptime(str(offer.start_time), date_format)
    #         b = datetime.datetime.strptime(str(offer.end_time), date_format)
    #
    #         delta = b - a
    #
    #         return delta
    #     else:
    #         print('offer not found')
    #         return False

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

    @property
    def wishlist(self):
        wishlists = Wishlist.objects.filter(buyer=self)
        return wishlists

    @property
    def order_products(self):
        orderproducts = Order_Product.objects.filter(buyer=self)
        return orderproducts

    def product_in_wishlist(self, product_id):
        product = Product.objects.filter(id=product_id).first()
        if product is None:
            return False
        wishlists = self.wishlist
        if wishlists.filter(product=product).count() > 0:
            return True
        return False



    @property
    def cart_total(self):
        total = 0
        for order_product in self.order_products:
            total += float(order_product.total)
        return total

    @property
    def cart_total_plus_vat(self):
        return self.cart_total * 1.16


    @property
    def vat_cost(self):
        total = 0
        for order_product in self.order_products:
            total += float(order_product.total)
        # print(total)
        vat = 0.16 * total
        # print(vat)
        return vat


    def product_wishlist_delete(self,product_id):
        product = Product.objects.filter(id=product_id).first()
        if product is not None:
            return True
        else:
            return False

    def product_in_cart(self, product_id):
        product = Product.objects.filter(id=product_id).first()
        if product is None:
            return False
        cart=self.order_products
        if cart.filter(product=product).count() > 0:
            return True
        return False






class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.FileField( default="no_products_image.jpg", upload_to='images')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s (%s)' % (self.image,(self.product.name))


class Review(models.Model):

    buyer= models.ForeignKey(Buyer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comments= models.TextField(max_length=100)
    ratings= models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s (%s)' % (self.comments, (self.ratings))

    @property
    def single_product_review(self):
        # product = Product.objects.filter(id=self.product)
        return product


class Wishlist(models.Model):
    product= models.ForeignKey(Product, on_delete=models.CASCADE)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s (%s)' % (self.buyer.first_name, (self.product.name))

class Region(models.Model):
    name=models.CharField(max_length=50, null=False)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, blank=False, null=False)
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
    status= models.CharField(choices=CHECKOUT_STATUS, max_length=100, default='UNVERIFIED')

    class Meta:
        verbose_name = 'Checkout'
        verbose_name_plural = 'Checkouts'

    def __str__(self):
        return '%s (%s)' % (self.buyer.first_name, (self.city))





class Order_Product(models.Model):
    product = models.ForeignKey(Product, related_name='orders', on_delete=models.CASCADE)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE, null=True, blank=True)
    quantity =  models.IntegerField(default=1)
    total = models.FloatField(max_length=100, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s %s(%s)' % (self.buyer.first_name, self.product.name, (self.quantity))





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
    status= models.CharField(choices=PAYMENT,max_length=100, default='UNVERIFIED')

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
    discount =models.FloatField(null=False, default=0)
    start_time = models.DateTimeField(default=datetime.datetime.now())
    end_time = models.DateTimeField(default=datetime.datetime.now())
    # duration=models.DateTimeField(default=datetime.datetime.now())     #  auto_now_add=True
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
            return '%s (%s)' % (self.product.name, (self.offer))

class Carousel(models.Model):
    image = models.ImageField(default="no_carousel.jpg", upload_to='couresel') #height_field=None, width_field=None,
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

    @property
    def variant_options(self):
        return Variant_Option.objects.filter(variant=self)

    def options(self):
        return Variant_Option.objects.filter(variant=self)

class Variant_Option(models.Model):
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s (%s)' % (self.variant.name, (self.name))

class OrderProductVariantOption(models.Model):
    orderProduct=models.ForeignKey(Order_Product,on_delete=models.CASCADE)
    variantOptions=models.ForeignKey(Variant_Option, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s %s' % (self.orderProduct.product.name, self.variantOptions.name)

class Product_Variant_Options(models.Model):
    product= models.ForeignKey(Product, on_delete=models.CASCADE)
    variant_options = models.ForeignKey(Variant_Option, on_delete=models.CASCADE ,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return '%s (%s)' % (self.product.name, (self.variant_options))

    def variant(self):
        return self.variant_options.variant








