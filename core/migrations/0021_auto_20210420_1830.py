# Generated by Django 3.1 on 2021-04-20 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_remove_payment_stripe_charge_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='phone_number',
            field=models.CharField(max_length=50),
        ),
    ]
