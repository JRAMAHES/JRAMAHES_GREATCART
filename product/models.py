from django.db import models
from category.models import Category
from django.urls import reverse

class Product(models.Model):
    product_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    dead_line = models.DateTimeField(null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)

    def get_url(self): 
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name

    def averageReview(self):
        from store.models import ReviewRating
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=models.Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReview(self):
        from store.models import ReviewRating
        reviews = ReviewRating.objects.filter(product=self, status=True).count()
        return reviews   