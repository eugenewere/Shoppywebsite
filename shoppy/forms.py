from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Buyer
from django import forms


class BuyerSignUpForm(UserCreationForm):

    class Meta:
        model = Buyer
        fields = ('username','first_name', 'last_name','phone_number',)

# class BuyerForm(forms.ModelForm):
#     # password = forms.CharField(widget=forms.PasswordInput())
#     # confirm_password = forms.CharField(widget=forms.PasswordInput())
#     # email=forms.CharField(widget=forms.EmailInput())
#     class Meta:
#         model=Buyer
#         fields=('first_name','last_name','phone_number','email','password')
#
#         # def clean(self):
#         #     cleaned_data = super(BuyerForm, self).clean()
#         #     password = cleaned_data.get("password")
#         #     confirm_password = cleaned_data.get("confirm_password")
#         #
#         #     if password != confirm_password:
#         #         raise forms.ValidationError(
#         #             "password and confirm_password does not match"
#         #         )
#         # def clean_email(self, *args, **kwargs):