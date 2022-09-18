from django.contrib import admin
from store_app.models import Products

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display=['product_name','price','stock','category','modified_date','is_available']
    prepopulated_fields={'slug':('product_name',)}

admin.site.register(Products,ProductAdmin)