# Generated by Django 3.0.3 on 2020-03-17 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mymac', '0009_order_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='amount',
            field=models.CharField(default=0, max_length=10),
        ),
    ]
