
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Buyer, Seller
from django import forms


class BuyerSignUpForm(UserCreationForm):

    class Meta:
        model = Buyer
        fields = ('username','first_name', 'last_name','phone_number',)



class BuyerUpdateForm(forms.ModelForm):

    class Meta:
        model = Buyer
        fields = ('username','first_name', 'last_name','phone_number',)









# seller
class SellerSignUpForm(UserCreationForm):

     class Meta:
         model = Seller
         fields = ('phone_number','business_no','store_logo','store_name','country','first_name','last_name','username',)


class SellerUpdateForm(forms.ModelForm):

    class Meta:
        model = Seller
        fields = ('phone_number','business_no','store_name','country','first_name','last_name','username',)

class SellerLogoUpdateForm(forms.ModelForm):

    class Meta:
        model=Seller
        fields=('store_logo',)