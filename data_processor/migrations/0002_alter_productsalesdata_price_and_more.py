# Generated by Django 5.1 on 2024-09-01 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_processor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productsalesdata',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
        migrations.AlterField(
            model_name='productsalesdata',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]
