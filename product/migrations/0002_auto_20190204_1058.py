# Generated by Django 2.1.5 on 2019-02-04 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='unit_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=19),
        ),
    ]