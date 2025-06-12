from django.contrib import admin
from .models import Variation

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active', 'updated_date', 'created_date')
    list_filter = ('product', 'variation_category', 'is_active')
    search_fields = ('product', 'variation_value')
    list_editable = ('is_active',)
    ordering = ('-created_date', "-updated_date")


admin.site.register(Variation, VariationAdmin)
