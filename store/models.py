from django.db import models
from product.models import Product

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=[
        ('color', 'color'),
        ('size', 'size'),
    ])
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    updated_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    objects = VariationManager()  # Custom manager for variations

    def __str__(self):
        return self.variation_value


