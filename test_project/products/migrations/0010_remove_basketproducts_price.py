# Generated by Django 5.0.1 on 2024-02-06 15:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_rename_total_sum_basketproducts_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basketproducts',
            name='price',
        ),
    ]
