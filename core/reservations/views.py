from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from core.reservations.models import *
from core.reservations.serializers import *
from core.utilis import LargeResultsSetPagination


@extend_schema(tags=['Reservations'])
class ReservationListAPIView(ListCreateAPIView):
    queryset = Reservation.objects.all().order_by('id')
    serializer_class = ReservationSerializer
    permission_classes = [AllowAny]
    pagination_class = LargeResultsSetPagination
