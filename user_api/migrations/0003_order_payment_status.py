# Generated by Django 4.1.4 on 2023-01-19 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_api', '0002_order_paymentmodel_orderitem_order_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_status',
            field=models.BooleanField(default=False),
        ),
    ]
