from django.urls import path

from core.reservations.views import *

urlpatterns = [
    path('reservations/', ReservationListAPIView.as_view(), name='reservation'),
    path('reservations/<int:pk>/', ReservationDetailAPIView.as_view(), name='reservation-detail'),
]