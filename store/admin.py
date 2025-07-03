from django.contrib import admin
from .models import Variation
from .models import ReviewRating

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active', 'updated_date', 'created_date')
    list_filter = ('product', 'variation_category', 'is_active')
    search_fields = ('product', 'variation_value')
    list_editable = ('is_active',)
    ordering = ('-created_date', "-updated_date")


class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'subject', 'rating', 'status', 'created_at', 'updated_at')
    list_filter = ('product', 'user', 'status')
    search_fields = ('product__name', 'user__username', 'subject')
    list_editable = ('status',)
    ordering = ('-created_at', '-updated_at')


admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating, ReviewRatingAdmin)
