from django.contrib import admin

# Register your models here.

# from .models import Product
# admin.site.register(Product)

from .models import Category, Tag, Product, StockAlert, Warehouse, WarehouseStock, StockTransaction


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'created_at')
    search_fields = ('name',)
    # ordering = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock')
    search_fields = ('name', 'category__name')
    list_filter = ('category', 'tags')


@admin.register(StockAlert)
class StockAlertAdmin(admin.ModelAdmin):
    list_display = ('product', 'alert_type', 'created_at')
    list_filter = ('alert_type',)
    search_fields = ('product__name',)


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'created_at')
    search_fields = ('name',)


@admin.register(WarehouseStock)
class WarehouseStockAdmin(admin.ModelAdmin):
    list_display = ('product', 'warehouse', 'stock')
    list_filter = ('warehouse', 'product')
    search_fields = ('product__name', 'warehouse__name')

    def save_model(self, request, obj, form, change):
        obj.handled_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(StockTransaction)
class StockTransactionAdmin(admin.ModelAdmin):
    list_display = ('product', 'warehouse', 'operation_type', 'quantity', 'handled_by', 'timestamp')
    list_filter = ('operation_type', 'warehouse', 'timestamp')
    search_fields = ('product__name', 'handled_by__username')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
