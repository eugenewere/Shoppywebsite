
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *
from django import forms


class BuyerSignUpForm(UserCreationForm):

    class Meta:
        model = Buyer
        fields = ('username','first_name', 'last_name','phone_number','email',)

class BuyerUpdateForm(forms.ModelForm):

    class Meta:
        model = Buyer
        fields = ('username','first_name', 'last_name','phone_number',)







# seller
class SellerSignUpForm(UserCreationForm):

     class Meta:
         model = Seller
         fields = ('email','phone_number','business_no','store_logo','store_name','country','first_name','last_name','username',)

    #seller update form


class SellerUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','username',)


class SellerForm(forms.ModelForm):
        class Meta:
            model = Seller
            fields = ('phone_number','business_no','store_logo','store_name','country',)









class ProductForm(forms.ModelForm):

    class Meta:
        model =Product
        fields= ('name', 'unit_cost','product_brand','short_description','long_description','featured_url','seller',)

class ImagesForm(forms.ModelForm):

    class Meta:
        model= Image
        fields=['image', 'product',]




class ProductVariantOptionForm(forms.ModelForm):

    class Meta:
        model= Product_Variant_Options
        fields =['product','variant_options',]



class InventoryForm(forms.ModelForm):

    class Meta:
        model = Inventory
        fields = ['product', 'quantity',]
class AddBrandForm(forms.ModelForm):

    class Meta:
        model =Brand
        fields =['name', 'category',]

class CarouselImageForm(forms.ModelForm):

    class Meta:
        model = Carousel
        fields = ['image','description',]

class RegionsForm(forms.ModelForm):

    class Meta:
        model = Region
        fields = ['name','region_cost','seller']

class VariantForm(forms.ModelForm):

    class Meta:
        model = Variant
        fields = ['name',]

class VariantOptionForm(forms.ModelForm):

    class Meta:
        model = Variant_Option
        fields = ['name','variant',]

class AddToWishList(forms.ModelForm):

    class Meta:
        model = Wishlist
        fields = ['buyer','product']

class OrderProductForm(forms.ModelForm):
     class Meta:
         model = Order_Product
         fields = ['quantity', 'product','buyer','total']

class OrderProductVariantOptionForm(forms.ModelForm):
     class Meta:
         model = OrderProductVariantOption
         fields =['orderProduct','variantOptions']

class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['name','parent_id']


class OfferForm(forms.ModelForm):

    class Meta:
        model= Offer
        fields = ['offer', 'product', 'discount', 'start_time', 'end_time',]

class ChangePasswordForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['password']