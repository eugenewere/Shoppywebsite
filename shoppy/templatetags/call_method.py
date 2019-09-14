import statistics

from django import template
from django.shortcuts import render_to_response
from django.views import View
from shoppy.models import *


register = template.Library()

@register.filter(name='has_buyer_ever_ordered')
def get_buyer_orders(product_id, user):
    buyer = Buyer.objects.filter(user_ptr_id=user.id).first()
    product=Product.objects.filter(id=product_id).first()
    if buyer is not None:
        ordered_product_review=Order_Product.objects.filter(checkout__isnull=False, buyer=buyer, product=product)
        return ordered_product_review
    else:
        return False



@register.filter(name='seller_orderd_products')
def get_seller_orders( user):
    seller= Seller.objects.filter(user_ptr_id=user.id).first()
    product =Product.objects.filter(seller=seller).all()
    if seller is not None:
        check_out_orders= Order_Product.objects.filter(checkout__isnull=False, product=product)

        return check_out_orders
    else:
        return False


@register.filter(name='seller_ordered_goods')
def ordered_products(product_id, user):
    seller = Seller.objects.filter(user_ptr_id=user.id).first()
    if seller is None:
        return False
    else:
        return seller.ordered_products(product_id)

@register.filter(name='average_ratings')
def average_ratings(product_id):
    product= Product.objects.filter(id=product_id).first()
    if product is None:
        return False
    else:
        data = []
        ratings=Review.objects.filter(product=product)
        for rating in ratings:
            data.append(rating.ratings)
        if data:
            average_ratings = statistics.mean(data)

            return average_ratings
        else:
            return 0


@register.filter(name='is_seller')
def is_seller(user):
    user_id=user.id
    seller = Seller.objects.filter(user_ptr_id=user_id).first()
    if seller is None:
        return False
    else:
        return True




@register.filter(name='wishlist_count')
def get_wishlist_count(user):

    buyer = Buyer.objects.filter(user_ptr_id=user.id).first()
    if buyer is not None:
        wishlist_count = Wishlist.objects.filter(buyer=buyer).count()
        return wishlist_count
    else:
        return False


@register.filter(name='is_product_in_wishlist')
def product_in_wishlist(product_id, user):
    buyer = Buyer.objects.filter(user_ptr_id=user.id).first()
    if buyer is None:
        return False
    else:
        return buyer.product_in_wishlist(product_id)


@register.filter(name='cart_count')
def get_cart_count(user):
    buyer = Buyer.objects.filter(user_ptr_id=user.id).first()
    if buyer is not None:
        cart_count =Order_Product.objects.filter(buyer=buyer).count()
        return cart_count
    else:
        return False


@register.filter(name='is_product_in_cart')
def product_in_cart(product_id, user):
    buyer = Buyer.objects.filter(user_ptr_id=user.id).first()
    if buyer is None:
        return False
    else:
        return buyer.product_in_cart(product_id)


@register.filter(name='total_cost_exclusive_vat')
def total_cost_exclusive_vat(user):
    """ Total cost of cart without VAT"""
    buyer = Buyer.objects.filter(user_ptr_id=user.id).first()
    if buyer is not None:
        return buyer.cart_total
    return False


@register.filter(name='total_cost_inclusive_of_vat')
def total_cost_inclusive_of_vat(user):
    """ Total cost of cart with 16% VAT"""
    buyer = Buyer.objects.filter(user_ptr_id=user.id).first()
    if buyer is not None:
        return buyer.cart_total_plus_vat
    return False


@register.filter(name='vat_cost')
def vat_cost(user):
    """ VAT Total cost of  16% """
    buyer = Buyer.objects.filter(user_ptr_id=user.id).first()
    if buyer is not None:
        return buyer.vat_cost
    return False

@register.filter(name='categories')
def categories(request):
    categories= Category.objects.filter(parent_id__isnull=True)
    # children_count = Category.objects.filter(id=categories)
    if categories is not None:
        return categories
    else:
        return False

@register.filter(name='product_on_offer')
def product_on_offer(product_id):
    now = datetime.datetime.now().date()
    offers=Offer.objects.filter(product=product_id, start_time__lte=now, end_time__gte=now)
    offerz= Offer.objects.filter(product=product_id).first()
    if offers is not None:
            # if offerz.end_time < now:
            #     offerz.delete()
        return offers
    else:
        return False

@register.filter(name='if_product_is_on_offer')
def if_product_is_on_offer(product_id):
    offers=Offer.objects.filter(product=product_id)
    if offers is not None:
        return offers
    else:
        return False


@register.filter(name='make_safe')
def make_safe(source):
    source = source.replace('/', '____')
    return "%s" %source






