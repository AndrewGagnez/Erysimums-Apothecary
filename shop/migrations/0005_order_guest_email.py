# Generated by Django 4.1.6 on 2023-03-14 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_order_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='guest_email',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]
