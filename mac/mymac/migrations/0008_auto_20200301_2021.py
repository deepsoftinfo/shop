# Generated by Django 3.0.3 on 2020-03-01 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mymac', '0007_orderupdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderupdate',
            name='order_id',
            field=models.IntegerField(default=''),
        ),
        migrations.AlterField(
            model_name='orderupdate',
            name='update_desc',
            field=models.CharField(max_length=5000),
        ),
    ]
