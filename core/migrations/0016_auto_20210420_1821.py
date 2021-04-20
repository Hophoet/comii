# Generated by Django 3.1 on 2021-04-20 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20201123_1637'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='being_delivered',
            new_name='delivered',
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('S', 'Shirt'), ('OW', 'Out Wear'), ('SH', 'Shoe'), ('NT', 'New Tech')], max_length=2, verbose_name='category'),
        ),
    ]