# Generated by Django 5.0.4 on 2024-05-05 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buyer', '0003_alter_buyer_buy_address_alter_buyer_buy_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesorder',
            name='razorpay_order_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='salesorder',
            name='razorpay_payment_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='salesorder',
            name='razorpay_payment_signature',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
