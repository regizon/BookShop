from django.db import models

from books.models import Book
from users.models import User


class StatusChoices(models.IntegerChoices):
    pending = 0
    paid = 1
    shipped = 2
    cancelled = 3

class StatusChoice(models.TextChoices):
    pending = 'pending'
    paid = 'paid'
    shipped = 'shipped'
    cancelled = 'cancelled'


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=StatusChoices, default=StatusChoices.pending)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
