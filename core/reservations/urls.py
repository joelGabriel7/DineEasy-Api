from django.urls import path

from core.reservations.views import *

urlpatterns = [
    path('reservations/', ReservationListAPIView.as_view(), name='index'),
]