# Generated by Django 5.1 on 2024-09-01 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_processor', '0003_alter_productsalesdata_review_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productsalesdata',
            name='review_count',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
