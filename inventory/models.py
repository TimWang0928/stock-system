from django.db import models


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
    min_stock = models.IntegerField(default=0, verbose_name="minimum stock")
    max_stock = models.IntegerField(default=100, verbose_name="maximum stock")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created at")

    def check_stock(self):
        if self.stock < self.min_stock:
            return 'low'
        elif self.stock > self.max_stock:
            return 'high'
        return 'normal'

    def __str__(self):
        return self.name


class StockAlert(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="product")
    alert_type = models.CharField(
        max_length=10,
        choices=[('low', 'minimum stock'), ('high', 'maximum stock')],
        verbose_name="alert type",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created at")

    def __str__(self):
        return f"{self.product.name} - {self.get_alert_type_display()} 告警"


class Warehouse(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="仓库名称")
    location = models.TextField(blank=True, verbose_name="仓库位置")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "仓库"
        verbose_name_plural = "仓库"

    def __str__(self):
        return self.name


class WarehouseStock(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name="商品")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, verbose_name="仓库")
    stock = models.IntegerField(default=0, verbose_name="库存数量")

    class Meta:
        unique_together = ('product', 'warehouse')  # 确保同一商品在同一仓库中只能有一条记录
        verbose_name = "仓库库存"
        verbose_name_plural = "仓库库存"

    def __str__(self):
        return f"{self.warehouse.name} - {self.product.name} 库存: {self.stock}"
