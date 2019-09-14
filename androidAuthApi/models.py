from django.db import models
from shoppy.models import Product, Category

# Create your models here.

class AndroidProducts(Product):
    category = models.ForeignKey(Category, related_name='androidproducts', on_delete=models.DO_NOTHING)
