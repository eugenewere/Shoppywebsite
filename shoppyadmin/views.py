
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render ,redirect ,HttpResponse

from django.template.loader import get_template
from django.views.generic.base import View

from rest_framework.views import APIView
from rest_framework.response import Response

from shoppy.forms import *
from shoppy.models import *


from shoppyadmin.utils import render_to_pdf

@login_required
def home(request):
    user=request.user.id
    logged_in_seller= Seller.objects.filter(user_ptr_id=user).first()
    seller = Seller.objects.all()
    products = Product.objects.filter(seller=logged_in_seller).order_by('-created_at')
    brand = Brand.objects.all()
    categories = Category.objects.all()
    buyers = Buyer.objects.all()
    orders = Order_Product.objects.filter(checkout__isnull=False)

    context = {
        'seller': seller,
        'products' : products,
        'brands' : brand,
        'categories' : categories,
        'buyers' : buyers,
        'orders': orders,

    }
    return render(request ,'index.html' ,context)

# product section
@login_required()
def view_all_products(request):
    if request.method == 'POST':
        # print(request.POST)
        # productVO = ProductVariantOptionForm(request.POST)
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            new_product = product_form.save()

            for upload in request.FILES.getlist('other_images[]'):
                image_file = {
                    'image': upload,
                }
                image_form = ImagesForm({'product': new_product.id}, image_file)
                image_form.save()

            for variant_option_id in request.POST.getlist('variant_options[]'):
                variant_option = Variant_Option.objects.filter(id=int(variant_option_id)).first()

                if variant_option is not None:
                    Product_Variant_Options.objects.create(
                        product=new_product,
                        variant_options=variant_option
                    )
            for inventory in request.POST['quantity']:
                if inventory is not None:
                    Inventory.objects.create(
                        product=new_product,
                        quantity=inventory,
                    )
            messages.success(request, 'Product Added Successfully')
        else:
           messages.error(request, 'Error Adding A Product')

    user = request.user.id
    logged_in_seller = Seller.objects.filter(user_ptr_id=user).first()
    products = Product.objects.filter(seller=logged_in_seller).order_by('-created_at')
    seller = Seller.objects.all()
    product = Product.objects.all()
    brand = Brand.objects.all()
    categories = Category.objects.all()

    variants =Variant.objects.all()
    # variantOptions = Variant_Option.objects.filter(variant=variants.id)
    # print(variantOptions)
    context = {
        'seller': seller,
        'products': products,
        'brands': brand,
        'categories': categories,
        # 'variantOptions':variantOptions,
        'variants': variants,
    }

    return render(request, 'products/view_products.html', context)

@login_required()
def edit_product(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    variants = Variant.objects.all()
    images = product.images
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES , instance=product)
        print(product_form)
        if product_form.is_valid():
           new_product = product_form.save()
           print(new_product)
           for upload in request.FILES.getlist('other_images[]'):
               print(upload)
               image_file = {
                   'image': upload,
               }
               image_form = ImagesForm({'product': new_product.id}, image_file)
               image_form.save()
               messages.success(request, 'Product Added Successfully')

    context = {
        'product': product,
        'images': images,
        'variants': variants,

    }

    return render(request, 'products/edit_products.html', context)

@login_required()
def product_delete(request, product_id):
    product = Product.objects.filter(id=product_id)
    product.delete()
    messages.success(request, 'Product Deleted Successfully')

    return redirect('ShoppyAdmin:shoppy_admin_view_all_products')

@login_required()
def image_delete(request, image_id):
    image = Image.objects.filter(id=image_id).first()
    if image is not None:
        product_id = image.product_id
        image.delete()
        messages.success(request, 'Image deleted successfully')

        return redirect('ShoppyAdmin:shoppy_admin_edit_product', product_id)


# brand section
@login_required()
def add_brand(request):
    if request.method == 'POST':
        brand_form = AddBrandForm(request.POST)

        if brand_form.is_valid():
            brand_form.save()
            messages.success(request, 'Brand Added Successfully')
            return redirect('ShoppyAdmin:shoppy_admin_add_brand')
        else:
            messages.error(request, 'Brand Not Added')
            return redirect('ShoppyAdmin:shoppy_admin_add_brand')

    brands = Brand.objects.all()
    categories = Category.objects.all()

    context = {
        'brands': brands,
        'categories': categories,
    }
    return render(request, 'brand and category/brand.html', context)

@login_required()
def brand_edit(request, brand_id):
    if request.method == 'POST':
        brand = Brand.objects.get(id=brand_id)
        form = AddBrandForm(request.POST, instance=brand)
        print(form)
        if form.is_valid():
            form.save()
            messages.success(request, 'Brand Update Successful')
            return redirect('ShoppyAdmin:shoppy_admin_add_brand')
        else:
            messages.error(request, 'Form Invalid')
            return redirect('ShoppyAdmin:shoppy_admin_add_brand')

@login_required()
def brand_delete(request, brand_id):
    brand = Brand.objects.filter(id=brand_id).first()
    brand.delete()
    messages.success(request, 'Brand Deleted Successfully')
    return redirect('ShoppyAdmin:shoppy_admin_add_brand')


# category section... this is to view category
@login_required()
def view_category(request):
    independent_categories = []
    categories = Category.objects.all()
    for category in categories:
        if not category.is_child:
            independent_categories.append(category)

    context = {
        'categories': set(independent_categories),
    }

    return render(request, 'brand and category/category.html', context)

@login_required()
def view_sub_category(request, category_id):
    sub_categories = Category.objects.filter(parent_id=category_id)
    categories = Category.objects.all()
    context = {
        "categories": categories,
        "sub_categories": sub_categories,
        # 'brand_count':new_brand_count,

    }

    return render(request, "brand and category/sub_categories.html", context)

@login_required()
def addingcategory(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category Added Successfully')
        else:
            messages.error(request, 'Category Not Added Successfully')
    return redirect('ShoppyAdmin:shoppy_admin_add_category')

@login_required()
def deletecategory(request, category_id):
    category = Category.objects.filter(id=category_id)
    category.delete()
    return redirect("ShoppyAdmin:shoppy_admin_add_category")

@login_required()
def editcategory(request, category_id):
    category = Category.objects.filter(id=category_id).first()
    categoryform = CategoryForm(request.POST, instance=category)
    if categoryform.is_valid():
        categoryform.save()
        messages.success(request, "Category updated successfully")
    else:
        messages.error(request, "Error Updating Category")
    return redirect("ShoppyAdmin:shoppy_admin_add_category")


# end of categories

# seller
@login_required()
def sellers(request):
    seller = Seller.objects.all()

    context = {
        'seller': seller,
    }
    return render(request, 'sellers.html', context)

@login_required()
def sellerStatusChange(request, seller_id):
    seller = Seller.objects.filter(id=seller_id).first()
    if seller.status == "UNVERIFIED":
        Seller.objects.filter(id=seller_id).update(
            status='VERIFIED'
        )
        messages.success(request, 'Seller Is Activated')
    else:
        Seller.objects.filter(id=seller_id).update(
            status='UNVERIFIED'
        )
        messages.success(request, 'Seller Is Deactivated')
    return redirect('ShoppyAdmin:shoppy-admin-sellers')


# seller

@login_required()
def orders(request):
    user = request.user.id
    seller = Seller.objects.filter(user_ptr_id=user).first()
    print(seller)

    orders = Order_Product.objects.filter(product__seller = seller, checkout__isnull=False)

    return render(request, 'orders.html',{'orders':orders})

@login_required()
def user_login(request):
    return render(request, 'login.html')

@login_required()
def reviews(request):
    comments = []
    user = request.user.id
    seller = Seller.objects.filter(user_ptr_id=user).first()
    reviews = Review.objects.filter(product__seller=user).first()
    products = Product.objects.filter(seller=seller)
    print(products)

    for product in products:
        review = Review.objects.filter(product=product).first()
        print(review)
        if review is not None:
            comments.append(review)
    context={
        'seller':seller,
        'reviews': set(comments)
    }
    return render(request, 'reviews.html', context)

@login_required()
def single_product_review(request, product_id):
    user = request.user.id
    reviews = Review.objects.filter(product__seller=user, product=product_id)
    proreview=Review.objects.filter(product=product_id).first()

    # product = Product.objects.filter(id=review.product.id)
    context = {
        'reviews': reviews ,
        'proreview':proreview,
    }

    return render(request, 'singleproductreviews.html', context)
def payments(request):
    return render(request, 'payments/payments.html')
@login_required()
def buyers(request):
    buyers = Buyer.objects.all()

    context = {
        'buyers': buyers,
    }
    return render(request, 'buyers.html', context)


@login_required()
def userAccount(request):
    user = request.user
    seller = Seller.objects.filter(user_ptr_id=user.id).first()

    if request.method == 'POST':
        seller_form = SellerForm(request.POST, request.FILES, instance=seller)

        seller_form.save()

        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        print(username)
        print(first_name)
        print(last_name)
        if seller is not None:
            user = User.objects.filter(pk=request.user.id).update(
                first_name=first_name,
                last_name=last_name,
                username=username
            )
            # user.first_name = first_name,
            # user.last_name = last_name,
            # user.username = username,
            # user.save()

        messages.success(request, 'Account Updated Successfully')
        return redirect("ShoppyAdmin:shoppy-user-account")

    context = {
        'seller': seller,
    }
    return render(request, 'useraccount.html', context)

def changepassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('ShoppyAdmin:shoppy-changepassword')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request,'accounts/changepassword.html',{'form':form})

# carousel
@login_required()
def view_carousel(request):
    if request.method == 'POST':
        carouselForm = CarouselImageForm(request.POST, request.FILES)
        print(carouselForm)
        if carouselForm.is_valid():
            carouselForm.save()
            messages.success(request, 'Carousel Image Added Successfully')
            return redirect('ShoppyAdmin:view_carousel')
        else:
            messages.error(request, 'Carousel Image not Added ')
            return redirect('ShoppyAdmin:view_carousel')

    else:
        carousels = Carousel.objects.all()
        carouselForm = CarouselImageForm()
        context = {
            'carousels': carousels,
            'form': carouselForm
        }

        return render(request, 'products/carousel.html', context)


def carousel_delete(request, carousel_id):
    carousel = Carousel.objects.filter(id=carousel_id).first()
    carousel.delete()
    messages.success(request, 'Carousel Image Deleted Succesfully')

    return redirect('ShoppyAdmin:view_carousel')


# end_of_carousel


# list,edit and delete regions
@login_required()
def view_regions(request):
    user=request.user.id
    seller =Seller.objects.filter(id=user).first()
    if request.method == 'POST':
        region=request.POST['name']
        region_cost = request.POST['region_cost']

        Region.objects.create(
            name=region,
            region_cost=region_cost,
            seller=seller,
        )
        messages.success(request, 'A Region And Its Respective Cost Has Been Added')
        return redirect("ShoppyAdmin:shoppy-admin-view-regions")



    regions = Region.objects.filter(seller=seller)
    sellers = Seller.objects.all()
    # print(sellers)
    context = {
        'regions': regions,
        'sellers': sellers,
    }
    return render(request, 'regions/regions.html', context)

@login_required()
def edit_regions(request, region_id):
    if request.method == 'POST':
        # regionId = Region.objects.filter(id=region_id).first()
        region = request.POST['name']
        region_cost = request.POST['region_cost']
        Region.objects.filter(id=region_id).update(
            name=region,
            region_cost=region_cost,
        )

        messages.success(request, 'Region Update Successful')
        return redirect('ShoppyAdmin:shoppy-admin-view-regions')

        # if region_form.is_valid():
        #     region_form.save()
        #     messages.success(request, 'Region Update Successful')
        #     return redirect('ShoppyAdmin:shoppy-admin-home')
        # else:
        #     messages.success(request, 'Region Error Updating')
        #     return redirect('ShoppyAdmin:shoppy-admin-home')

@login_required()
def delete_regions(request, region_id):
    region = Region.objects.filter(id=region_id).first()
    region.delete()
    messages.success(request, 'Region Deleted Successfully')
    return redirect('ShoppyAdmin:shoppy-admin-view-regions')


# end_of_regions


# variant,variantoptions ( add,delete,edit)
@login_required()
def variants(request):
    if request.method == 'POST':
        variant_form = VariantForm(request.POST)
        if variant_form.is_valid():
            print(variant_form)
            variant_form.save()
            messages.success(request, 'Variant Added Successfully')
            return redirect('ShoppyAdmin:variants')
        else:
            messages.error(request, 'Error Adding Variants')
            return redirect('ShoppyAdmin:variants')
    variants = Variant.objects.all()
    variant_options = Variant_Option.objects.all()
    context = {
        'variants': variants,
        'variant_options': variant_options,
    }
    return render(request, 'variants/variants.html', context)

@login_required()
def variant_delete(request, variant_id):
    variant = Variant.objects.filter(id=variant_id).first()
    variant.delete()
    messages.success(request, 'Variant Deleted Successfully')
    return redirect('ShoppyAdmin:variants')


def variant_edit(request, variant_id):
    if request.method == 'POST':
        variant = Variant.objects.filter(id=variant_id).first()
        variant_form = VariantForm(request.POST, instance=variant)
        if variant_form.is_valid():
            variant_form.save()
            messages.success(request, 'Variant Update Successful')
            return redirect('ShoppyAdmin:variants')
        else:
            messages.success(request, 'Variant Error Updating')
            return redirect('ShoppyAdmin:variants')

@login_required()
def variants_options(request):
    if request.method == 'POST':
        variantOptions = VariantOptionForm(request.POST)
        if variantOptions.is_valid():
            variantOptions.save()
            messages.success(request, 'Variant Options Added Successfully')
            return redirect('ShoppyAdmin:variants')
        else:
            messages.error(request, 'Variant Option Not Added')

@login_required()
def variants_options_edit(request, variant_option_id):
    if request.method == 'POST':
        variant_option = Variant_Option.objects.filter(id=variant_option_id).first()
        variant_option_form = VariantOptionForm(request.POST, instance=variant_option)
        print(variant_option_form)
        if variant_option_form.is_valid():
            variant_option_form.save()
            messages.success(request, 'Variant Options Update Successful')
            return redirect('ShoppyAdmin:variants')
        else:
            messages.success(request, 'Variant Options Error Updating')
            return redirect('ShoppyAdmin:variants')

@login_required()
def variants_options_delete(request, variant_option_id):
    variantOption = Variant_Option.objects.filter(id=variant_option_id).first()
    variantOption.delete()
    messages.success(request, 'Variant Option Deleted Successfully')
    return redirect('ShoppyAdmin:variants')


# end_of_variant


# featuredproducts
def featured_products(request):
    user = request.user.id
    featured_products = Product.objects.filter(status="FEATURED", seller=user)
    context = {
        'products': featured_products,
    }

    return render(request, 'products/featuredproducts.html', context)

@login_required()
def featured_products_featured(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    if product.status == "FEATURED":
        Product.objects.filter(id=product_id).update(status="NORMAL")
        messages.success(request, 'Product Status Is Updated to Normal Successfully')
    return redirect('ShoppyAdmin:shoppy_admin_view_all_products')

@login_required()
def normal_products_normal(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    if product.status == "NORMAL":
        Product.objects.filter(id=product_id).update(status="FEATURED")
        messages.success(request, 'Product Status Is Updated to Featured Successfully')
    return redirect('ShoppyAdmin:shoppy_admin_view_all_products')

# end of featured products
# offer
@login_required()
def offer(request):
    user=request.user.id
    products = Product.objects.filter(seller=user)
    offers=Offer.objects.filter(product__seller=user).order_by('-created_at')

    context = {
        'products': products,
        'offers': offers,
    }
    return render(request, 'products/productoffers.html', context)
@login_required()
def addOffer(request):

    if request.method == 'POST':
        # print(request.POST)
        form = OfferForm(request.POST)

        print(form)
        if form.is_valid():
            form.save()
            messages.success(request, 'Offer Successfully Been Made')
            return redirect('ShoppyAdmin:view_product_offer')
        messages.error(request, 'Error Adding An Offer')
        return redirect('ShoppyAdmin:view_product_offer')

    return redirect('ShoppyAdmin:view_product_offer')
@login_required()
def editOffer(request,offer_id):
    offer =Offer.objects.filter(id=offer_id).first()
    if offer:
        form = OfferForm(request.POST, instance=offer)
        if request.method == 'POST':
            if form.is_valid():
               form.save()
               messages.success(request, "Offer Updated Successfully")
               return redirect('ShoppyAdmin:view_product_offer')
            else:
                messages.error(request, "Offer Not Updated Successfully")
                return redirect('ShoppyAdmin:view_product_offer')
    else:
        messages.error(request,"Offer Not Found")
        return redirect('ShoppyAdmin:view_product_offer')
@login_required()
def deleteOffer(request, offer_id):
    offer =Offer.objects.filter(id=offer_id).first()

    if offer:

        offer.delete()
        messages.success(request,'Offer Deleted Successfuly')
        return redirect('ShoppyAdmin:view_product_offer')
    else:
        messages.error(request, 'Error! Offer Not Found')
        return redirect('ShoppyAdmin:view_product_offer')



# offer
@login_required()
def viewAllReports(request):

    return render(request,'reports/reports.html')
# reports

class GeneratePDF(View):
    def get(self, request, *args, **kwargs):
        orders = Order_Product.objects.filter(checkout__isnull=False)
        template = get_template('invoice.html')
        context = {
            'orders': orders,
        }
        html = template.render(context)
        pdf = render_to_pdf('invoice.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" % ("12341231")
            content = "inline; filename='%s'" % (filename)
            # download = request.GET.get("download")
            response['Content-Disposition'] = content
            # if download:
            #     content = "attachment; filename='%s'" % (filename)
            return pdf
        return HttpResponse("Not found")

class GenerateProductPDF(View):
    def get(self, request, *args, **kwargs):
        user = request.user.id
        products =Product.objects.filter(seller=user)
        template = get_template('productspdf.html')
        context = {
            'products': products,
        }
        html = template.render(context)
        pdf = render_to_pdf('productspdf.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" % ("12341231")
            content = "inline; filename='%s'" % (filename)
            # download = request.GET.get("download")
            response['Content-Disposition'] = content
            # if download:
            #     content = "attachment; filename='%s'" % (filename)
            return pdf
        return HttpResponse("Not found")

# reports

class ListUsers(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, format=None):
        sellers=Seller.objects.all().count()
        buyers=Buyer.objects.all().count()


        labels = ['Sellers','Buyers']
        defaultData = [sellers, buyers]
        context={
            'labels':labels,
            'defaultData':defaultData,

        }
        return Response(context)

class ListOrders(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, format=None):
        user=request.user.id

        month_data = []
        months_choices=[]
        months_choices_int=[]
        for i in range(1,13):
            months_choices.append(( datetime.date(2008, i, 1).strftime('%B')[0:3]))
        labels2 = months_choices
        for z in range(1,13):
            months_choices_int.append((datetime.date(2008, z, 1).strftime('%m')))
        for months_choice in months_choices_int:
            month_data.append(Order_Product.objects.filter(checkout__isnull=False, created_at__month=months_choice, product__seller=user).count())
        defaultData2 = month_data
        context2={
            'labels2':labels2,
            'defaultData2':defaultData2,

        }

        month_data = {}



        return Response(context2)