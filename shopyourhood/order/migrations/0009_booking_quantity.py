# Generated by Django 5.1.2 on 2025-05-24 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_booking_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
