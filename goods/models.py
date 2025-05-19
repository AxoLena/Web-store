from django.db import models
from django.urls import reverse

class Categories(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')

    class Meta:
        db_table = 'category'
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return f'Name: {self.name}  |   Slug: {self.slug}'

class Products(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    description = models.TextField(blank=True, null=True)
    composition = models.TextField(blank=True,null=True)
    image = models.ImageField(upload_to='goods_images', blank=True, null=True)
    price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2)
    discount = models.DecimalField(default=0.00, max_digits=7,decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(to=Categories, on_delete=models.SET_DEFAULT, default=None)
    class Meta:
        db_table = 'product'
        verbose_name = 'product'
        verbose_name_plural = 'products'
        ordering = ('id', )

    def __str__(self):
        return f'Name: {self.name}  |   Category: {self.category.name}'

    def get_absolute_url(self):
        return reverse('goods:product', kwargs={'product_slug': self.slug})

    def display_id(self):
        return f'{self.id:05}'

    def discount_price(self):
        if self.discount:
            return round((self.price - self.price * self.discount/100), 2)
        return self.price