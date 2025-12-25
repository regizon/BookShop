from django.db import models

from books.models import Book
from users.models import User


class Cart(models.Model):
    customer = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    session_id = models.CharField(max_length=100, blank=True, null=True)
    constraints = [
        models.CheckConstraint(
            name="%(app_label)s_%(class)s_thing1_or_thing2",
            condition=(
                    models.Q(customer__isnull=True, session_id__isnull=False)
                    | models.Q(customer__isnull=False, session_id__isnull=True)
            ),
        )
    ]

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.IntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['cart', 'book'],
                name='unique_cart_item'
            )
        ]