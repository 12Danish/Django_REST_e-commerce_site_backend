from django.contrib import admin
from .models import Product, Review


class ReviewInline(admin.StackedInline):
    model = Review
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'owner', 'category', 'price', 'n_bought', 'discount', 'date_created', 'sale_item', 'sale_price',
        )
    inlines = [ReviewInline]


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'reviewer', 'name', 'stars', 'product', 'body')


admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)

# Register your models here.
