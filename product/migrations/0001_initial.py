# Generated by Django 2.1.5 on 2019-01-28 08:37

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('active_ingredients', models.TextField()),
                ('expiry_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('quantity', models.PositiveIntegerField()),
                ('total_price', models.DecimalField(decimal_places=2, editable=False, max_digits=19)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Product')),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=19)),
                ('total_stock', models.PositiveIntegerField(default=0, editable=False)),
                ('total_stock_value', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=19)),
                ('current_stock', models.PositiveIntegerField(default=0, editable=False)),
                ('current_stock_value', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=19)),
                ('sold_stock', models.PositiveIntegerField(default=0, editable=False)),
                ('sold_stock_value', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=19)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='product.Product')),
            ],
        ),
    ]
