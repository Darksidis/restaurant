from django.db import models
from django.urls import reverse


# Create your models here.


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status_published='published')


class TypeTable(models.Model):
    type = models.CharField('Тип столика', max_length=266)

    def __str__(self):
        return self.type


class Client(models.Model):
    """Данные пользователей, которые хоть раз забронировали столик."""

    name = models.CharField('Имя клиента', max_length=124)
    email = models.CharField('Почта', max_length=124)
    phone = models.CharField('Телефон', max_length=124)

    def __str__(self):
        return 'Забронировано клиентом {}'.format(self.name)


class Table(models.Model):
    """ Данные о бронирований столиков."""

    STATUS_PUBLISHED = (
        ('draft', 'Закрыт для бронирования'),
        ('published', 'Открыт'),
    )
    number = models.IntegerField('Номер', unique=True)
    type = models.ForeignKey(TypeTable, on_delete=models.CASCADE)
    seats = models.IntegerField('Количество стульев')
    booking_price = models.FloatField('Цена бронирования')
    status_booking = models.ForeignKey(Client, on_delete=models.SET_NULL, blank=True, null=True)
    status_published = models.CharField(
        'Доступ к столику',
        max_length=128,
        choices=STATUS_PUBLISHED,
        default='published',
    )

    objects = models.Manager()

    published = PublishedManager()

    def get_absolute_url(self):
        "Метод возвращает с помощью функций reverse() ссылку на cтолик"
        return reverse('booking:table_detail', args=[self.number])

    def __str__(self):
        return 'Столик под номером {}'.format(self.number)
