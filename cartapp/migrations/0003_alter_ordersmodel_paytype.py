# Generated by Django 4.2.19 on 2025-03-02 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartapp', '0002_ordersmodel_payment_completed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordersmodel',
            name='paytype',
            field=models.CharField(default='Paypal', max_length=50),
        ),
    ]
