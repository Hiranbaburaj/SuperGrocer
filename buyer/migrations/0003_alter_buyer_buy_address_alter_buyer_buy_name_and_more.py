# Generated by Django 5.0.3 on 2024-04-21 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buyer', '0002_salesorder_orderitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyer',
            name='buy_address',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='buyer',
            name='buy_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='buyer',
            name='buy_phone',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
