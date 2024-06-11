import uuid

from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('cancelled', 'Cancelled'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('pending_accept', 'Pending Accepted'),
        ('cancelled', 'Cancelled'),
        ('appeal', 'Appeal'),
        ('appeal_consider', 'Appeal Consideration'),
    ]

    # Уникальный идентификатор
    # id = models.IntegerField()
    #
    idx = models.CharField(default=uuid.uuid4(), primary_key=True, max_length=255)

    # Тип груза
    cargo_type = models.CharField(default="object", max_length=255)

    # Маршрут: От - До
    cargo_inf_to = models.CharField(max_length=255)
    cargo_inf_from = models.CharField(max_length=255)

    # Описание (Объем и размер)
    cargo_inf_size = models.CharField(max_length=255)
    cargo_inf_wht = models.CharField(max_length=255)

    # Время отправки
    cargo_deliv_start_at = models.DateTimeField()
    cargo_deliv_end_at = models.DateTimeField()

    # Статус
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='pending_accept')

    # Описание
    description = models.TextField()

    # Комментарий
    comment = models.TextField()

    # Отправитель (клиент)
    client = models.ForeignKey(User, related_name='client_orders', on_delete=models.CASCADE)

    # Перевозчик (курьер)
    courier = models.ForeignKey(User, related_name='courier_orders', null=True, blank=True,
                                on_delete=models.SET_NULL)

    # Автоматические временные метки
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_offers(self):
        return self.offers.all()

    def __str__(self):
        return '%s — %s | %s | %s | Отправление: %s / [%s - %s]' % (
        self.cargo_inf_from, self.cargo_inf_to, self.cargo_type, self.status, self.cargo_deliv_start_at, self.client,
        self.courier)


#
class OffersOrder(models.Model):
    idx = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='offers')
    offer_amount = models.DecimalField(max_digits=10, decimal_places=2)
    offer_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offers_made')

    def __str__(self):
        return f'Offer {self.idx} for Order {self.order.id} by User {self.user.id} with amount {self.offer_amount}'
