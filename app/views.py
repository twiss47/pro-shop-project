from django.shortcuts import render, get_object_or_404
from .models import Category,Product


def index(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        'categories':categories,
        'products':products
    }
    return render(request, 'app/home.html', context)



def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'app/product_detail.html', {'product':product})



def category_products(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = category.products.all() 
    categories = Category.objects.all() 
    context = {
        'products': products,
        'categories': categories,
        'selected_category': category
    }
    return render(request, 'app/home.html', context)
