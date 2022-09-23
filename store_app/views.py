from http.client import HTTPResponse
from itertools import product
import keyword
from multiprocessing import context
from unicodedata import category
from django.shortcuts import render,get_object_or_404
from category.models import Category
from store_app.models import Products
from cart_app.models import CartItem,Cart
from cart_app.views import _cart
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.http import HttpResponse

# Create your views here.
def store(request,category_slug=None):
    if category_slug!=None:
        categories=get_object_or_404(Category,slug=category_slug)
        products=Products.objects.all().filter(category=categories,is_available=True).order_by('id')
        paginator=Paginator(products,2)
        page_number=request.GET.get('page')
        page_obj=paginator.get_page(page_number)
        product_count=products.count()
    else:    
        products=Products.objects.all().filter(is_available=True).order_by('id')
        paginator=Paginator(products,6)
        page_number=request.GET.get('page')
        page_obj=paginator.get_page(page_number)
        product_count=products.count()
    context={
        'products':page_obj,
        'product_count':product_count
    }
    return render(request,'store_app/store.html',context)

def product_detail(request,category_slug,product_slug):
    try:
        single_product=Products.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart=CartItem.objects.filter(product=single_product,cart__cartid=_cart(request)).exists()
    except Exception as e:
        raise e
    context={
        'product':single_product,
         'in_cart':in_cart,
    }
    return render(request,'store_app/product_detail.html',context)

def search1(request):
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']
        if keyword:
            products=Products.objects.order_by('created_date').filter(description__icontains=keyword)
            product_count=products.count()
        context={
            'products':products,
            'product_count':product_count,
        }
    return render(request,'store_app/store.html',context)