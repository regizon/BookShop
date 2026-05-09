from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0008_collection_bookcollection'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='discount_price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
