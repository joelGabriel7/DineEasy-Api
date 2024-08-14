from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.restaurant.models import Restaurant
from core.restaurant.serializers import RestaurantSerializers
from core.utilis import *


@extend_schema(tags=['Restaurantes'])
class RestaurantListAPIView(ListCreateAPIView):
    queryset = Restaurant.objects.all().order_by('id')
    serializer_class = RestaurantSerializers
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    filter_backends = [SearchFilter]
    search_fields = ['rnc', 'name', 'email', 'phone']
    pagination_class = LargeResultsSetPagination

    @extend_schema(
        summary="Listar restaurantes",
        description="Obtiene una lista de todos los restaurantes.",
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        summary="Crear restaurante",
        description="Crea un nuevo restaurante o varios restaurantes si se proporciona una lista.",
    )
    def post(self, request, *args, **kwargs):
        is_many = isinstance(request.data, list)
        if is_many:
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save()


@extend_schema(tags=['Restaurantes'])
class RestaurantRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializers
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    @extend_schema(
        summary="Obtener restaurante",
        description="Obtiene los detalles de un restaurante específico.",
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Actualizar restaurante",
        description="Actualiza todos los campos de un restaurante específico.",
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(
        summary="Actualizar parcialmente restaurante",
        description="Actualiza parcialmente los campos de un restaurante específico.",
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Eliminar restaurante",
        description="Elimina un restaurante específico.",
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "deleted restaurant successfully"}, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        instance.delete()
