# Generated by Django 3.1 on 2021-04-20 18:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_payment_phone_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='stripe_charge_id',
        ),
    ]
