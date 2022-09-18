from unicodedata import category
from django.shortcuts import render,get_object_or_404
from category.models import Category
from store_app.models import Products

# Create your views here.
def store(request,category_slug=None):
    if category_slug!=None:
        categories=get_object_or_404(Category,slug=category_slug)
        products=Products.objects.all().filter(category=categories,is_available=True)
        product_count=products.count()
    else:    
        products=Products.objects.all().filter(is_available=True)
        product_count=products.count()
    context={
        'products':products,
        'product_count':product_count
    }
    return render(request,'store_app/store.html',context)

def product_detail(request,category_slug,product_slug):
    try:
        single_product=Products.objects.get(category__slug=category_slug,slug=product_slug)
    except Exception as e:
        raise e
    context={
        'product':single_product
    }
    return render(request,'store_app/product_detail.html',context)