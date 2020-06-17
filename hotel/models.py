from django.db import models
from django.conf import settings


# Create your models here.
class Nutrient(models.Model):
    nutrient_name = models.CharField(max_length=50, unique = True)
    nutrient_unit = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.nutrient_name

class Product(models.Model):
    name = models.CharField(max_length=50,unique = True)
    description = models.TextField()
    status = models.BooleanField(default= False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    nutrients = models.ManyToManyField(Nutrient, through="ProductNutrients")

    def __str__(self):
        return self.name

class ProductNutrients(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    nutrient = models.ForeignKey('Nutrient', on_delete=models.PROTECT)
    nutrient_value = models.DecimalField(max_digits=19, decimal_places=10, default= 0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ('product', 'nutrient')

    def __str__(self):
        return str(self.nutrient_value)

