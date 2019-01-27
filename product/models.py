import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.dispatch import receiver
from djmoney.models.fields import MoneyField

from .validators import validate_quantity_in_sale


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    active_ingredients = models.TextField()
    expiry_date = models.DateField()


class Stock(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=19, decimal_places=2)
    total_stock = models.PositiveIntegerField(default=0, editable=False)
    total_stock_value = models.DecimalField(
        default=0, editable=False, max_digits=19, decimal_places=2)
    current_stock = models.PositiveIntegerField(default=0, editable=False)
    current_stock_value = models.DecimalField(
        default=0, editable=False, max_digits=19, decimal_places=2)
    sold_stock = models.PositiveIntegerField(default=0, editable=False)
    sold_stock_value = models.DecimalField(
        default=0, editable=False, max_digits=19, decimal_places=2)

    def clean(self):
        try:
            self.current_stock = self.total_stock - self.sold_stock
            self.total_stock_value = self.total_stock * self.unit_price
            self.current_stock_value = self.current_stock * self.unit_price
            self.sold_stock_value = self.sold_stock * self.unit_price
        except:
            raise ValidationError('An error occurred')


class Sale(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(
        editable=False, max_digits=19, decimal_places=2)

    def clean_quantity(self):
        try:
            if self.quantity > self.product.stock.current_stock:
                raise Exception()
            self.total_price = self.product.stock.unit_price * self.quantity
        except Exception:
            raise ValidationError(f'''
                Only {self.product.stock.current_stock} of this product are left
            ''')


@receiver(models.signals.post_save, sender=Sale)
def update_stock_on_sale(sender, instance, created, **kwargs):
    if created:
        instance.product.stock.sold_stock += instance.quantity
        instance.product.stock.save()
