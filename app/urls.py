from django.urls import path,include
from .views import index,detail,login_view, register_view, logout_view, add_product, delete_product, edit_product

app_name = 'app'

urlpatterns = [
    path('',index,name='index'),
    path('category/<int:category_id>',index,name='products_of_category'),
    path('detail/<product_id>',detail,name='detail'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('product/add/', add_product, name='add_product'),
    path('edit/<int:pk>/', edit_product, name='edit_product'),
    path('delete/<int:pk>/',delete_product, name='delete_product'),
]

