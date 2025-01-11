from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Product, StockAlert, WarehouseStock, StockTransaction


@receiver(post_save, sender=Product)
def stock_alert_handler(sender, instance, **kwargs):
    stock_status = instance.check_stock()

    if stock_status == 'low':
        StockAlert.objects.create(product=instance, alert_type='low')
        # print(f"低库存告警：{instance.name} 库存低于 {instance.min_stock}")

    elif stock_status == 'high':
        StockAlert.objects.create(product=instance, alert_type='high')
        # print(f"高库存告警：{instance.name} 库存高于 {instance.max_stock}")


@receiver(pre_save, sender=WarehouseStock)
def generate_stock_transaction(sender, instance, **kwargs):

    if instance.pk:
        original = WarehouseStock.objects.get(pk=instance.pk)
        if instance.stock != original.stock:
            operation_type = 'IN' if instance.stock > original.stock else 'OUT'
            quantity = abs(instance.stock - original.stock)

            StockTransaction.objects.create(
                product=instance.product,
                warehouse=instance.warehouse,
                operation_type=operation_type,
                quantity=quantity,
                handled_by=instance.handled_by,
                remarks="auto recording"
            )
    else:
        operation_type = 'IN'
        quantity = instance.stock


        StockTransaction.objects.create(
            product=instance.product,
            warehouse=instance.warehouse,
            operation_type=operation_type,
            quantity=quantity,
            handled_by=instance.handled_by,
            remarks="auto recording"
        )