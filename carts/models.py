from django.db import models
from product.models import Product
from store.models import Variation  # Assuming Variation is in store app
from django.shortcuts import get_object_or_404, redirect
from accounts.models import Account  # Assuming Account is in accounts app

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)  # Assuming Account is in accounts app
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation = models.ManyToManyField('store.Variation', blank=True)  # Assuming Variation is in store app
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity


    def __str__(self):
        return f"{self.product})"