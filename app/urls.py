from django.urls import path
from django.views.i18n import set_language

from .views import (
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    OrderCreateView,
    ContactView,
)

app_name = 'app'

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),

    path(
        'category/<int:category_id>/',
        ProductListView.as_view(),
        name='products_of_category'
    ),

    path(
        'product/<int:pk>/',
        ProductDetailView.as_view(),
        name='detail'
    ),

    path(
        'product/<int:pk>/order/',
        OrderCreateView.as_view(),
        name='order'
    ),

    path(
        'add/',
        ProductCreateView.as_view(),
        name='add_product'
    ),

    path(
        'edit/<int:pk>/',
        ProductUpdateView.as_view(),
        name='edit_product'
    ),

    path(
        'delete/<int:pk>/',
        ProductDeleteView.as_view(),
        name='delete_product'
    ),

    path(
        'contact/',
        ContactView.as_view(),
        name='contact'
    ),

    path(
        'set-language/',
        set_language,
        name='set_language'
    ),
]
