import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.dispatch import receiver
from djmoney.models.fields import MoneyField


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    active_ingredients = models.TextField()
    expiry_date = models.DateField()

    def __str__(self):
        return self.name


class Stock(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    unit_price = models.DecimalField(
        default=0, max_digits=19, decimal_places=2)
    total_stock = models.PositiveIntegerField(default=0, editable=False)
    total_stock_value = models.DecimalField(
        default=0, editable=False, max_digits=19, decimal_places=2)
    current_stock = models.PositiveIntegerField(default=0)
    current_stock_value = models.DecimalField(
        default=0, editable=False, max_digits=19, decimal_places=2)
    sold_stock = models.PositiveIntegerField(default=0, editable=False)
    sold_stock_value = models.DecimalField(
        default=0, editable=False, max_digits=19, decimal_places=2)

    def save(self, *args, **kwargs):
        # self.current_stock = self.total_stock - self.sold_stock
        # self.total_stock_value = self.total_stock * self.unit_price
        self.current_stock_value = self.current_stock * self.unit_price
        self.sold_stock_value = self.sold_stock * self.unit_price
        super(Stock, self).save(*args, **kwargs)
    

    def __str__(self):
        return self.product.name

class GroupSale(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    total_price = models.DecimalField(default=0, editable=False, max_digits=19, decimal_places=2)
    purchase_time = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        pass


class Sale(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    group_sale = models.ForeignKey(GroupSale, on_delete=models.CASCADE)
    total_price = models.DecimalField(
        editable=False, max_digits=19, decimal_places=2)

    def clean(self):
        try:
            if self.quantity > self.product.stock.current_stock:
                raise Exception
            self.total_price = self.product.stock.unit_price * self.quantity
        except Exception:
            if self.product.stock.current_stock == 0:
                error_message = f'{self.product.name} is out of stock'
            elif self.product.stock.current_stock == 1:
                error_message = f'Only {self.product.stock.current_stock} of {self.product.name} is left'
            else:
                error_message = f'Only {self.product.stock.current_stock} of {self.product.name} are left'
            raise ValidationError(error_message)
    
    def __str__(self):
        return str(self.id)


@receiver(models.signals.post_save, sender=Product)
def add_stock_on_add_product(sender, instance, created, **kwargs):
    if created:
        Stock.objects.create(product=instance)


@receiver(models.signals.post_save, sender=Sale)
def update_stock_on_sale(sender, instance, created, **kwargs):
    if created:
        instance.product.stock.sold_stock += instance.quantity
        instance.product.stock.save()
