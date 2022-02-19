from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from book.models import Book
from django.utils import timezone
from datetime import timedelta
import uuid

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    authority_zarinpal = models.CharField(default='', max_length=255)
    ref_if_zarinpal = models.CharField(default='', max_length=255)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user} - {self.id}'

    def get_total_price(self):
        return sum([item.book.price for item in self.items.all()])


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='order_item')
    link_download = models.CharField(default='', max_length=255)
    expire_token = models.DateTimeField(default=timezone.now() + timedelta(days=1))

    def __str__(self):
        return f'{self.book.title}'


@receiver(post_save, sender=Order)
def update_order(sender, instance, *args, **kwargs):
    if instance.paid:
        for item in instance.items.all():
            item.link_download = settings.DEFAULT_DOMAIN + "download" + "/" + uuid.uuid4() + "/"
            item.expire_token = timezone.now() + timedelta(days=1)
            item.save()

