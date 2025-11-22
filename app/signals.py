from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Product, Order


@receiver(post_save, sender=Product)
def product_save(sender, instance, created, **kwargs):
    if created:
        print(f'[LOG] New product added:{instance.name}')
    
    else:
        print(f'[LOG] product updated:{instance.name}')


def decrease_product_stock(sender, instance, created, **kwargs):
    if created:
        product = instance.product
        product.stock -= instance.quantity
        product.save()

        print(f"[STOCK] {instance.quantity} removed from {product.name}")


@receiver(post_delete, sender=Order)
def restore_product_stock(sender, instance, **kwargs):
    product = instance.product
    product.stock += instance.quantity
    product.save()

    print(f"[STOCK] Restored {instance.quantity} to {product.name}")

