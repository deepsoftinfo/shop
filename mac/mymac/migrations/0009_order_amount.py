# Generated by Django 3.0.3 on 2020-03-02 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mymac', '0008_auto_20200301_2021'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='amount',
            field=models.IntegerField(default=0),
        ),
    ]