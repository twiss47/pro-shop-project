from django.contrib import admin
from .models import Category, Product, Comment, Order
from modeltranslation.admin import TranslationAdmin


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    ordering = ('title',)


class ProductAdmin(TranslationAdmin):  
    list_display = ('name', 'price', 'stock', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('price', 'stock')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Product, ProductAdmin)  

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'email', 'created_at')
    search_fields = ('name', 'email', 'text')
    list_filter = ('created_at', 'product')
    ordering = ('-created_at',)


@admin.register(Order)
class OrderAdmin(TranslationAdmin,admin.ModelAdmin):
    list_display = ('product', 'name', 'phone', 'quantity', 'created_at')
    search_fields = ('name', 'phone', 'product__name')
    list_filter = ('created_at', 'product')
    ordering = ('-created_at',)



try:
    admin.site.unregister(Order)
except:
    pass

admin.site.register(Order, OrderAdmin)