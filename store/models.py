from django.db import models
from accounts.models import Account
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


# *************** CREATING REVIEWRATING MODEL ******************
class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)  # True for approved, False for not approved
    helpful = models.IntegerField(default=0)  # Count of helpful votes
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

# *************** END OF CREATING REVIEWRATING MODEL ******************