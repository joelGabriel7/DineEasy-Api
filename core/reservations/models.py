from datetime import datetime
from django.db import models
from django.dispatch import receiver
from django.forms import model_to_dict
from core.customers.models import CustomerUser
from core.restaurant.models import Restaurant, Table
from django.db.models.signals import post_save


class Reservation(models.Model):
    STATUS_RESERVATIONS = [
        ('confirmed', 'Confirmado'),
        ('pending', 'Pendiente'),
        ('cancell', 'Cancelada'),
        ('waiting_list', 'Lista de espera')
    ]

    customer = models.ForeignKey(CustomerUser, on_delete=models.CASCADE, verbose_name='Cliente')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, verbose_name='Restaurante')
    date = models.DateField(verbose_name='Fecha de la reservacion', default=datetime.now)
    time = models.TimeField(verbose_name='Fecha de la reservacion', default=datetime.now)
    party_size = models.IntegerField(verbose_name='Cantidad de personas')
    special_request = models.CharField(max_length=255, null=True, blank=True, verbose_name='Peticion especial')
    status = models.CharField(max_length=15, choices=STATUS_RESERVATIONS, default='pending')

    def toJSON(self):
        item = model_to_dict(self)
        item['date'] = self.date.strftime('%Y-%m-%d')
        item['time'] = self.time.strftime('%H:%M:%S%p')
        item['restaurant'] = self.restaurant.toJSON()
        return item

    class Meta:
        verbose_name = 'Reservacion'
        verbose_name_plural = 'Reservaciones'
        ordering = ['date']
        db_table = 'reservations'


class TableReservations(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE, verbose_name='Mesa')
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, verbose_name='Reservaciones')

    def __str__(self):
        return f'Reservation {self.reservation.date} - Table {self.table} '

    class Meta:
        verbose_name = 'Mesa reservada'
        verbose_name_plural = 'Mesas reservadas'
        db_table = 'mesas_reservations'
        ordering = ['table']


@receiver(post_save, sender=Reservation)
def assignTable(sender, instance=None, created=False, **kwargs):
    if created and instance.status == 'confirmed':
        avaible_tables = Table.objects.filter(
            restaurant=instance.restaurant,
            capacity__gte=instance.party_size,
            status='F'
        ).order_by('capacity')

        if avaible_tables.exists():
            table = avaible_tables.first()
            TableReservations.objects.create(table=table, reservation=instance)
            table.status = 'O'
            table.save()
        else:
            instance.status = 'waiting_list'
            instance.save()