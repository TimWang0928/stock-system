from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product, StockAlert


@receiver(post_save, sender=Product)
def stock_alert_handler(sender, instance, **kwargs):
    stock_status = instance.check_stock()

    if stock_status == 'low':
        StockAlert.objects.create(product=instance, alert_type='low')
        # print(f"低库存告警：{instance.name} 库存低于 {instance.min_stock}")

    elif stock_status == 'high':
        StockAlert.objects.create(product=instance, alert_type='high')
        # print(f"高库存告警：{instance.name} 库存高于 {instance.max_stock}")
