# Generated by Django 5.0.1 on 2024-02-03 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='address',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='seller',
            name='company_name',
            field=models.CharField(default=None, max_length=255),
        ),
    ]
