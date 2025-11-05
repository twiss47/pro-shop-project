from django.urls import path
from django.conf import settings
from .views import index, product_detail, category_products
app_name = 'app'

urlpatterns = [
    path('',index,name="index"),
    path('product/<int:pk>/', product_detail, name='product_detail'),
    path('category/<int:category_id>/', category_products, name='category_products'),


]

