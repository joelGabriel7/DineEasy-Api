from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token


class CustomerUser(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Número telefoníco')
    preferences = models.JSONField(max_length=500, null=True, blank=True, verbose_name='Preferencias del cliente')

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        db_table = 'Customer'


@receiver(post_save, sender=CustomerUser)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
