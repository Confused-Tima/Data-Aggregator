# Generated by Django 5.1 on 2024-09-01 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_processor', '0002_alter_productsalesdata_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productsalesdata',
            name='review_count',
            field=models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=8, null=True),
        ),
    ]
