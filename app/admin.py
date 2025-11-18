from django.contrib import admin
from .models import Category, Product, Comment, Order


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    ordering = ('title',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('price', 'stock')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    prepopulated_fields = {'slug': ('name',)}  # agar slug bo‘lsa


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'email', 'created_at')
    search_fields = ('name', 'email', 'text')
    list_filter = ('created_at', 'product')
    ordering = ('-created_at',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'phone', 'quantity', 'created_at')
    search_fields = ('name', 'phone', 'product__name')
    list_filter = ('created_at', 'product')
    ordering = ('-created_at',)
