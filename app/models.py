from django.db import models
from decimal import Decimal
from django.templatetags.static import static
from django.utils.text import slugify


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class Category(BaseModel):
    title = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = 'Categories'


class Product(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, null=False, unique=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=14, decimal_places=2)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    stock = models.PositiveSmallIntegerField(default=1)
    discount = models.PositiveSmallIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 related_name='products',
                                 null=True, blank=True)    
    
    @property
    def discounted_price(self):
        if self.discount:
            return self.price * Decimal(f'{(1 - self.discount / 100)}')
        return self.price
    
    @property
    def get_image_url(self):
        if not self.image:
            return static('app/images/not_found.jpg')
        return self.image.url
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Comment(BaseModel):
    class RatingChoices(models.IntegerChoices):
        ONE = 1, "⭐ 1"
        TWO = 2, "⭐⭐ 2"
        THREE = 3, "⭐⭐⭐ 3"
        FOUR = 4, "⭐⭐⭐⭐ 4"
        FIVE = 5, "⭐⭐⭐⭐⭐ 5"
    
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    message = models.TextField()
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='comments')
    file = models.ImageField(upload_to='comments/%Y/%m/%d/',null=True,blank=True)
    rating = models.PositiveSmallIntegerField(choices=RatingChoices.choices,default = RatingChoices.FIVE)
    is_handle = models.BooleanField(default=False)
    
    

    def __str__(self):
        return f'{self.name} - {self.message}'


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.product.name} by {self.name}"






class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject