import datetime
from typing import Iterable
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, EmailValidator
from django.forms import model_to_dict
from config.settings import MEDIA_URL, STATIC_URL
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _


def validate_rnc(value):
    if len(value) != 9 and len(value) != 11:
        raise ValidationError("El RNC debe tener 9 u 11 dígitos.")


class Restaurant(models.Model):
    STATUS_CHOICES = [
        ('active', 'Activo'),
        ('inactive', 'Inactivo'),
        ('renovating', 'En Renovación'),
    ]

    rnc = models.CharField(
        max_length=15,
        unique=True,
        error_messages={
            "unique": "Este RNC ya existe, por favor ingrese otro."
        },
        help_text="This fields is for the rnc of restaurant",
        verbose_name="RNC",
        validators=[validate_rnc]
    )
    logo = models.ImageField(
        upload_to='restaurant/%Y/%m/%d',
        null=True,
        blank=True,
        verbose_name='Logo del restaurante'
    )
    name = models.CharField(
        max_length=255,
        verbose_name='Nombre restaurant',
        help_text="This is for name of restaurants",
    )
    address = models.CharField(
        max_length=255,
        verbose_name='Direccion restaurant',
        help_text="This is for address of restaurants",
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='Numero del restaurant',
        help_text="This is for number of restaurants",
        unique=True,
        validators=[RegexValidator(r'^\+?1?\d{9,10}$',
                                   message="El número de teléfono debe estar en el formato: '+999999999'. Se permiten hasta 10 dígitos.")]
    )
    email = models.EmailField(
        max_length=255,
        verbose_name='Email del restaurants',
        validators=[EmailValidator(message='Ingrese una dirección de email válida.')],
        unique=True
    )
    capacity = models.PositiveIntegerField(
        verbose_name='Capacidad',
        help_text="Capacidad total del restaurante",
    )
    opening_time = models.TimeField(
        verbose_name='Hora de apertura',
        default=datetime.time(0, 0)
    )
    closing_time = models.TimeField(
        verbose_name='Hora de cierre',
        default=datetime.time(0, 0)

    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name='Estado'
    )
    create_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    update_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de modificacion'
    )

    def __str__(self):
        return self.name

    def get_logo(self):
        if self.logo:
            return f'{MEDIA_URL}{self.logo}'
        return f'{STATIC_URL}img/img.png'

    def is_open(self):
        now = timezone.localtime().time()
        return self.opening_time <= now <= self.closing_time

    @property
    def operation_duration(self):
        return datetime.combine(datetime.date.min, self.closing_time) - datetime.combine(datetime.date.min,
                                                                                         self.opening_time)

    def toJSON(self):
        item = model_to_dict(self, exclude=['logo'])
        item['opening_time'] = self.opening_time.strftime('%H:%M')
        item['closing_time'] = self.closing_time.strftime('%H:%M')
        item['create_at'] = self.create_at.strftime('%Y-%m-%d %H:%M:%S')
        item['update_at'] = self.update_at.strftime('%Y-%m-%d %H:%M:%S')
        item['logo'] = self.get_logo()
        return item

    class Meta:
        verbose_name = 'Restaurante'
        verbose_name_plural = 'Restaurantes'
        ordering = ['name']
        db_table = 'restaurant'

    def save(self, *args, **kwargs):
        self.get_logo()
        return super().save(*args, **kwargs)


class Table(models.Model):
    class Status(models.TextChoices):
        OCCUPIED = 'O', _('Ocupada')
        FREE = 'F', _('Libre')
        UNPAID = 'U', _('Sin pagar')

    restaurant = models.ForeignKey(
        'Restaurant',
        on_delete=models.CASCADE,
        verbose_name=_('Restaurante'),
        related_name='tables'
    )
    number = models.PositiveIntegerField(
        verbose_name=_('Número de mesa'),
        validators=[MinValueValidator(1)]
    )
    capacity = models.PositiveIntegerField(
        verbose_name=_('Cantidad de asientos'),
        validators=[MinValueValidator(1)]
    )
    location = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_('Ubicación')
    )
    status = models.CharField(
        max_length=1,
        choices=Status.choices,
        default=Status.FREE,
        verbose_name=_('Estado')
    )

    class Meta:
        verbose_name = _('Mesa')
        verbose_name_plural = _('Mesas')
        ordering = ['number']
        db_table = _('Mesas')

    def __str__(self):
        return f"{self.restaurant.name} - Mesa {self.number}"

    @classmethod
    def get_summary(cls, restaurant_id):
        tables = cls.objects.filter(restaurant_id=restaurant_id)
        total_tables = tables.count()
        occupied_tables = tables.filter(status=cls.Status.OCCUPIED).count()
        free_tables = tables.filter(status=cls.Status.FREE).count()
        unpaid_tables = tables.filter(status=cls.Status.UNPAID).count()

        return {
            'total_tables': total_tables,
            'occupied_tables': occupied_tables,
            'free_tables': free_tables,
            'unpaid_tables': unpaid_tables
        }
