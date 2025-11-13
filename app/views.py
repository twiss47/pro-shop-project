from .models import Category , Product
from django.http import JsonResponse
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProductForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Product, Comment, Order
from .utils import filter_product
from django.db.models import Q




def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
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
    search_query = request.GET.get('q','')
    filter_type = request.GET.get('filter_type','')

    if category_id:
        products = Product.objects.filter(category = category_id)
    else:
        products = Product.objects.all()

    if search_query:
        products = products.filter(Q(name__icontains = search_query) | Q(description__icontains=search_query))


    products = filter_product(filter_type,products)

    
    context = {
        'categories':categories,
        'products':products
    }
    return render(request,'app/home.html',context)






def detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    comments = product.comments.all().order_by('-created_at')

    if request.method == "POST":
        if 'order_submit' in request.POST:
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            quantity = int(request.POST.get('quantity', 1))

            if quantity > product.stock:
                messages.error(request, f"Sorry, only {product.stock} items in stock!")
            else:
                Order.objects.create(product=product, name=name, phone=phone, quantity=quantity)
                product.stock -= quantity
                product.save()
                messages.success(request, "Your order has been placed successfully!")
                return redirect('app:detail', pk=pk)

        elif 'comment_submit' in request.POST:
            name = request.POST.get('name')
            email = request.POST.get('email')
            text = request.POST.get('text')
            Comment.objects.create(product=product, name=name, email=email, text=text)
            return redirect('app:detail', pk=pk)

    context = {
        'product': product,
        'comments': comments
    }
    return render(request, 'app/detail.html', context)




def superuser_required(user):
   return user.is_superuser


@user_passes_test(superuser_required)
def add_product(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('app:index')
    return render(request, 'app/product_form.html', {'form': form, 'title': 'Add Product'})




@user_passes_test(superuser_required)
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('app:index')
    return render(request, 'app/delete_product.html', {'product': product})


@user_passes_test(superuser_required)
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('app:index')
    else:
        form = ProductForm(instance=product)

    return render(request, 'app/edit_product.html', {'form': form, 'product': product})



def comment_view(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        text = request.POST.get('text')

        if name and email and text:
            Comment.objects.create(name=name, email=email, text=text)
        return redirect('app:comment')
    
    comments = Comment.objects.all().order_by('-created_at')
    return render(request, 'app/comments.html', {'comments': comments})
        