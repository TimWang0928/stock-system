from django.db import models


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="category name")
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="parent category",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created at")

    # class Meta:
    #     verbose_name = "分类"
    #     verbose_name_plural = "分类"

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="tag name")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created at")

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="product name")
    description = models.TextField(blank=True, verbose_name="product description")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="category"
    )
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="tag")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="price")
    stock = models.PositiveIntegerField(verbose_name="stock")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created at")

    def __str__(self):
        return self.name
