import json

from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.restaurant.models import Table, Restaurant
from core.restaurant.serializers import TableSerializer, TableSummarySerializer
from core.utilis import *


@extend_schema(tags=['Mesas'])
class TableListCreateView(ListCreateAPIView):
    queryset = Table.objects.all().order_by('id')
    serializer_class = TableSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    search_fields = ['capacity', 'location', 'status']
    filter_backends = [SearchFilter]
    pagination_class = LargeResultsSetPagination

    @extend_schema(
        summary="Listar Mesas",
        description="Obtiene una lista de todas las mesas de un restarante.",
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        summary="Crear Mesas",
        description="Crea una nueva mesa o varias mesa si se proporciona una lista",
    )
    def post(self, request, *args, **kwargs):
        is_many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=is_many)

        if not serializer.is_valid():

            if 'non_field_errors' in serializer.errors:
                errors = serializer.errors['non_field_errors'][0]
            else:
                errors = json.dumps(serializer.errors)
            return Response({"detail": errors}, status=status.HTTP_400_BAD_REQUEST)
        try:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def perform_create(self, serializer):
        serializer.save()


@extend_schema(tags=['Mesas'])
class TableByRestaurant(GenericAPIView):
    serializer_class = TableSerializer
    queryset = Table.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    @extend_schema(
        summary="Obtener una Mesa por restaurante",
        description="Obtiene los detalles de una Mesa específico por restaurantes",
    )
    def get(self, request, pk):
        restaurant = get_object_or_404(Restaurant, pk=pk)
        tables = self.get_queryset().filter(restaurant=restaurant)
        serializer = self.get_serializer(tables, many=True)
        return Response(serializer.data)


@extend_schema(tags=['Mesas'])
class TableRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    @extend_schema(
        summary="Obtener una Mesa",
        description="Obtiene los detalles de una Mesa específico.",
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Actualizar una Mesa",
        description="Actualiza todos los campos de una Mesa específico.",
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(
        summary="Actualizar parcialmente una Mesa",
        description="Actualiza parcialmente los campos de una Mesa específico.",
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Eliminar una Mesa",
        description="Elimina una Mesa específico.",
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "deleted table successfully"}, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        instance.delete()


@extend_schema(tags=['Mesas'])
class TableSummaryApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    @extend_schema(
        summary="Resumen de Mesas",
        description="Obtiene un resumen del estado de las mesas para un restaurante específico.",
        responses={200: TableSummarySerializer}
    )
    def get(self, request, restaurant_id):
        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
        except Restaurant.DoesNotExist:
            return Response({'error': "Restaurant does not exist"}, status=status.HTTP_404_NOT_FOUND)

        table_summary = Table.get_summary(restaurant_id)

        data = {
            'restaurant_id': restaurant_id,
            'restaurant_name': restaurant.name,
            'summary': table_summary
        }

        serializer = TableSummarySerializer(data=data)
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
