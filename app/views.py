from .models import Category , Product
from django.http import JsonResponse
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProductForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Product




def register_view(request):
    if request.method == 'Post':
        form = RegisterForm(request.Post)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request,'Successfully Registered')
            return redirect('home')
    
    else:
        form = RegisterForm()
    return render(request,'app/register.html', {'form':form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}!')
            return redirect('app:index')
    else:
        form = LoginForm()
    return render(request, 'app/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You logged out')
    return redirect('app:login')



def index(request,category_id = None):
    
    categories = Category.objects.all()
    
    if category_id:
        products = Product.objects.filter(category = category_id)
    else:
        products = Product.objects.all()
    
    
    context = {
        'categories':categories,
        'products':products
    }
    return render(request,'app/home.html',context)



def detail(request,product_id):
    product = Product.objects.get(id = product_id)
    if not product:
        return JsonResponse(data={'message':'Sorry :(  Page Not Found','status_code':404})
    
    context = {
        'product' : product
    }
    return render(request,'app/detail.html',context)



def superuser_required(view_func):
    decorated_view_func = user_passes_test(lambda u: u.is_superuser, login_url='app:login')(view_func)
    return decorated_view_func

@user_passes_test(superuser_required)
@superuser_required
def add_product(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('app:index')
    return render(request, 'app/product_form.html', {'form': form, 'title': 'Add Product'})

@user_passes_test(superuser_required)
@superuser_required
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect('app:index')
    return render(request, 'app/product_form.html', {'form': form, 'title': 'Update Product'})

@user_passes_test(superuser_required)
@superuser_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('app:index')
    return render(request, 'app/product_confirm_delete.html', {'product': product})
