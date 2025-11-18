from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q

from .models import Category, Product, Comment, Order
from .forms import RegisterForm, LoginForm, ProductForm, OrderModelForm
from .utils import filter_product


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Successfully Registered')
            return redirect('app:index')
    else:
        form = RegisterForm()

    return render(request, 'app/register.html', {'form': form})





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





def index(request, category_id=None):
    categories = Category.objects.all()
    search_query = request.GET.get('q', '')
    filter_type = request.GET.get('filter_type', '')

    if category_id:
        products = Product.objects.filter(category=category_id)
    else:
        products = Product.objects.all()

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    products = filter_product(filter_type, products)

    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'app/home.html', context)




def detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    comments = product.comments.all().order_by('-created_at')
    order_form = OrderModelForm()

    # COMMENT YOZISH
    if request.method == "POST" and 'comment_submit' in request.POST:
        name = request.POST.get('name')
        email = request.POST.get('email')
        text = request.POST.get('text')

        Comment.objects.create(
            product=product,
            name=name,
            email=email,
            text=text
        )
        messages.success(request, "Your comment has been added!")
        return redirect('app:detail', pk=pk)

    context = {
        'product': product,
        'comments': comments,
        'order_form': order_form,
    }
    return render(request, 'app/detail.html', context)




def create_order(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = OrderModelForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            order.product = product

            if order.quantity > product.stock:
                messages.error(request, "Not enough quantity!", extra_tags='order')
            else:
                product.stock -= order.quantity
                product.save()
                order.save()
                messages.success(request, "Order successfully sent! ✅", extra_tags='order')
                return redirect('app:detail', pk=pk)
        else:
            messages.error(request, "Formda xatolik bor", extra_tags='order')

    return redirect('app:detail', pk=pk)



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
