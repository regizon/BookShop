from django.db import models
from books.models import Book
from users.models import User


class DeliveryStatusChoice(models.TextChoices):
    pending = 'pending'
    shipped = 'shipped'
    cancelled = 'cancelled'


class PaymentStatusChoice(models.TextChoices):
    paid = 'paid'
    unpaid = 'unpaid'
    failed = 'failed'
    refunded = 'refunded'
    partially_refunded = 'partially_refunded'


class DeliveryChoice(models.TextChoices):
    self = 'self'
    courier = 'courier'


class PaymentMethodChoice(models.TextChoices):
    online = 'online'
    offline = 'offline'

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_status = models.CharField(choices=DeliveryStatusChoice, default=DeliveryStatusChoice.pending)
    payment_status = models.CharField(choices=PaymentStatusChoice, default=PaymentStatusChoice.unpaid)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    comments = models.TextField(blank=True)
    delivery_type = models.CharField(choices=DeliveryChoice)
    payment_method = models.CharField(choices=PaymentMethodChoice)
    email = models.CharField(max_length=25, blank=True)
    phone = models.CharField(max_length=12)
    city = models.CharField(max_length=30, blank=True)
    street = models.CharField(max_length=30, blank=True)
    house = models.PositiveSmallIntegerField(null=True)
    apartment = models.PositiveSmallIntegerField(null=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
