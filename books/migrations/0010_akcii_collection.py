from django.db import migrations


def create_akcii_collection(apps, schema_editor):
    Collection = apps.get_model('books', 'Collection')
    Collection.objects.get_or_create(name='Акції')


def reverse_akcii_collection(apps, schema_editor):
    Collection = apps.get_model('books', 'Collection')
    Collection.objects.filter(name='Акції').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0009_book_discount_price'),
    ]

    operations = [
        migrations.RunPython(create_akcii_collection, reverse_akcii_collection),
    ]
