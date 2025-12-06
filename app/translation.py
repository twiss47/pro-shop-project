from modeltranslation.translator import translator, TranslationOptions
from .models import Product, Comment, Order, Contact



class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'description')




translator.register(Product, ProductTranslationOptions)





class OrderTranslationOptions(TranslationOptions):
    fields = ('name',) 

translator.register(Order, OrderTranslationOptions)