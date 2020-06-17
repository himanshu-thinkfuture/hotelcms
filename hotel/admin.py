from django.contrib import admin

from .models import Nutrient, Product, ProductNutrients



admin.site.register(Nutrient)
admin.site.register(Product)
admin.site.register(ProductNutrients)