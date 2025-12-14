from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, DeleteView, UpdateView, View
)
from django.contrib import messages
from django.db.models import Q, Avg
from django.contrib.auth.mixins import UserPassesTestMixin

from .models import Category, Product, Comment, Order, Contact
from .forms import ProductForm, OrderModelForm
from .utils import filter_product

class ProductListView(ListView):
    model = Product
    template_name = 'app/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = Product.objects.annotate(
            avg_rating=Avg('comments__rating')
        )

        category_id = self.kwargs.get('category_id')
        search_query = self.request.GET.get('q')
        filter_type = self.request.GET.get('filter_type')

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        return filter_product(filter_type, queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'app/detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        return Product.objects.annotate(
            avg_rating=Avg('comments__rating')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object

        product.avg_rating = int(product.avg_rating or 0)

        context['comments'] = Comment.objects.filter(
            product=product
        ).order_by('-created_at')

        context['related_products'] = Product.objects.filter(
            category=product.category
        ).exclude(id=product.id)[:4]

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        email = request.POST.get("email")
        if not email:
            messages.error(request, "Email is required!")
            return redirect('app:detail', pk=self.object.pk)

        Comment.objects.create(
            product=self.object,
            name=request.POST.get("name"),
            email=email,
            rating=request.POST.get("rating", 5),
            message=request.POST.get("message"),
            file=request.FILES.get("file")
        )

        return redirect('app:detail', pk=self.object.pk)

class OrderCreateView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
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

        else:
            messages.error(request, "Form Error", extra_tags='order')

        return redirect('app:detail', pk=pk)



class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser
    

class ProductCreateView(SuperuserRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name ='app/product_form.html'
    success_url = reverse_lazy('app:index')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)    
        context['title'] = 'Add Product'
        return context



class ProductDeleteView(SuperuserRequiredMixin, DeleteView):
    model = Product
    template_name = 'app/delete_product.html'
    success_url = reverse_lazy('app:index')



class ProductUpdateView(SuperuserRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'app/edit_product.html'
    success_url = reverse_lazy('app:index')



def realted_prodcuts(product, limit:4):
    return Product.objects.filter(
        category = product.category
    ).exclude(id=product.id)[limit:4]


class ContactView(View):
    def get(self, request):
        return render(request, 'app/contact.html')

    def post(self, request):
        data = (
            request.POST.get("name"),
            request.POST.get("email"),
            request.POST.get("subject"),
            request.POST.get("message"),
        )

        if not all(data):
            messages.error(request, "All fields are required!")
            return redirect(request.META.get('HTTP_REFERER'))

        Contact.objects.create(
            name=data[0],
            email=data[1],
            subject=data[2],
            message=data[3]
        )

        messages.success(request, "Your message has been sent successfully!")
        return redirect(request.META.get('HTTP_REFERER'))
