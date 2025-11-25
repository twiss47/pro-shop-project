from django.urls import path,include
from .views import index,detail, add_product, delete_product, edit_product, contact_view

app_name = 'app'

urlpatterns = [
    path('',index,name='index'),
    path('category/<int:category_id>',index,name='products_of_category'),
    path('product/<int:pk>/', detail, name='detail'),
    path('product/add/', add_product, name='add_product'),
    path('edit/<int:pk>/', edit_product, name='edit_product'),
    path('delete/<int:pk>/',delete_product, name='delete_product'),
     path('contact/', contact_view, name='contact'),
]

