from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, GenericAPIView,  get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from core.reservations.serializers import *
from core.restaurant.models import Restaurant
from core.utilis import LargeResultsSetPagination


@extend_schema(tags=['Reservations'])
class ReservationListAPIView(ListCreateAPIView):
    queryset = Reservation.objects.all().order_by('id')
    serializer_class = ReservationSerializer
    permission_classes = [AllowAny]
    pagination_class = LargeResultsSetPagination

    @extend_schema(
        summary='Listar las reservaciones',
        description='Retorna un listado de las reservaciones disponibles o canceladas'

    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary='Crea una reservacion',
        description='Creada una reservacion'
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


@extend_schema(tags=['Reservations'])
class GetReservationStatus(ListAPIView):
    queryset = Reservation.objects.all().order_by('id')
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = LargeResultsSetPagination
    filter_backends = [SearchFilter]
    search_fields = ['status']

    @extend_schema(
        summary="Lista las Reservaciones por su status",
        description="Obtiene una lista de todas las reservaciones por el status que se ingreso",
    )
    def get(self, request, *args, **kwargs):
        term = self.request.query_params.get('search', '')
        reservation = self.get_queryset().filter(status=term)
        if not reservation:
            return Response({"message": f"No se encontraron reservaciones con el status '{term}'"},
                            status=status.HTTP_404_NOT_FOUND)
        return super().get(request, *args, **kwargs)


@extend_schema(tags=['Reservations'])
class ReservationDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Reservation.objects.all().order_by('id')
    serializer_class = ReservationSerializer
    permission_classes = [AllowAny]
    pagination_class = LargeResultsSetPagination

    @extend_schema(
        summary="Obtener una reservacion",
        description="Obtiene una reservacion especifica",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary='Actualiza una reservacion',
        description='Actualiza una reservacion especifica',
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary='Actualiza una reservacion parcialmente',
        description='Actualiza una reservacion parcialmente',
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        summary='Elimina una reservacion ',
        description='Actualiza una reservacion',
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
