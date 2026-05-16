from django.db.models.signals import post_save
from django.dispatch import receiver

from books.models import Book, BookCollection


@receiver(post_save, sender=Book)
def remove_from_collections_on_zero_quantity(sender, instance, **kwargs):
    if instance.quantity == 0:
        BookCollection.objects.filter(book=instance).delete()
