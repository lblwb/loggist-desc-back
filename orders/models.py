import uuid

from django.db import models
from django.contrib.auth.models import User


# Заявки
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
    # id = models.BigIntegerField()
    #
    idx = models.CharField(default=uuid.uuid4(), primary_key=False, max_length=255)

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

    # offers = models.ManyToManyField('OffersOrder', related_name='offers')

    # Автоматические временные метки
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def get_offers(self):
    #     return self.offers.all()

    def __str__(self):
        return '%s — %s | %s | %s | Отправление: %s / [%s - %s]' % (
            self.cargo_inf_from, self.cargo_inf_to, self.cargo_type, self.status, self.cargo_deliv_start_at,
            self.client,
            self.courier)


# Офферы к заявке
class OffersOrder(models.Model):
    class Meta:
        db_table = 'orders_offers'

    # id = models.BigIntegerField()

    # Уникальный идентификатор
    idx = models.CharField(default=uuid.uuid4(), primary_key=False, max_length=255)

    # Связь с заявкой
    # order = models.ForeignKey(Order, related_name='offers', on_delete=models.CASCADE)

    order = models.ForeignKey(Order, related_name='offers',blank=True, on_delete=models.CASCADE, )
    # Другие поля

    # Сумма оффера
    offer_amount = models.DecimalField(max_digits=10, decimal_places=2)

    # Дата оффера
    offer_date = models.DateTimeField(auto_now_add=True)

    # Пользователь, сделавший оффер
    courier = models.ForeignKey(User, related_name='courier_offer', null=True, blank=True,
                                on_delete=models.SET_NULL)

    def __str__(self):
        # return f'Offer {self.idx} for Order {self.order.idx} by User {self.courier.id} with amount {self.offer_amount}'
        return f'Предложение -- %s — %s | %s ' % (self.idx, self.courier, self.offer_amount)


# Чат заявки
class OrderChat(models.Model):
    class Meta:
        db_table = 'orders_chats'

    # id = models.BigIntegerField()
    #
    idx = models.CharField(default=uuid.uuid4(), primary_key=False, max_length=255)

    # Связь с заявкой

    order = models.ForeignKey(Order, related_name='chats', blank=True, on_delete=models.CASCADE)

    # Связь с клиентом
    client = models.ForeignKey(User, related_name='client_chats', on_delete=models.CASCADE)

    # Связь с курьером
    courier = models.ForeignKey(User, related_name='courier_chats', null=True, blank=True, on_delete=models.SET_NULL)

    # Автоматические временные метки
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Chat for Order %s between %s and %s' % (self.order.idx, self.client, self.courier)


# Чат - Сообщения - по заявке
class OrderChatMsg(models.Model):

    class Meta:
        db_table = 'orders_chats_msgs'

    # Связь с чатом
    chat = models.ForeignKey(OrderChat, related_name='messages', blank=True, on_delete=models.CASCADE)

    # Отправитель
    sender = models.ForeignKey(User, on_delete=models.CASCADE)

    # Сообщение
    message = models.TextField()

    # Время отправки
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Message from %s in Chat %s' % (self.sender, self.chat.id)
