from django.contrib.auth.models import Group
from django.utils.text import slugify
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth.hashers import make_password
from core.customers.models import CustomerUser
from core.restaurant.models import Restaurant, Table
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Ejemplo de Restaurante',
            summary='Datos de muestra de un restaurante',
            description='Este es un ejemplo de los datos de un restaurante',
            value={
                'rnc': '401-8765-43',
                'name': 'El Sabor Tropical',
                'address': 'Avenida del Sol 234',
                'phone': '8298765432',
                'email': 'info@sabortropical.com',
                'capacity': 70,
                'opening_time': '10:00:00',
                'closing_time': '22:30:00',
            },
            request_only=False,
            response_only=False,
        ),
    ]
)
class RestaurantSerializers(serializers.ModelSerializer):


    user_password = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = Restaurant
        fields = ['id', 'rnc', 'name', 'address', 'logo', 'phone', 'email', 'capacity', 'opening_time', 'closing_time','user_password']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['create_at'] = instance.create_at.strftime("%Y-%m-%d %H:%M:%S")
        representation['update_at'] = instance.update_at.strftime("%Y-%m-%d %H:%M:%S")
        if instance.logo:
            representation['logo'] = instance.logo.url
        representation['logo'] = instance.get_logo()
        return representation

    def create(self, validated_data):
        user_password = validated_data.pop('user_password', None)
        if not user_password:
            user_password = validated_data['rnc']

        restaurant = Restaurant.objects.create(**validated_data)
        user = CustomerUser.objects.create(
            username=validated_data['name'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            password=make_password(user_password)
        )

        restaurant_group, _ = Group.objects.get_or_create(name='restaurant')
        user.groups.add(restaurant_group)

        return restaurant

# class RestaurantSerializers(serializers.ModelSerializer):
#     user_password = serializers.CharField(write_only=True, required=False)
#
#     class Meta:
#         model = Restaurant
#         fields = ['id', 'rnc', 'name', 'address', 'logo', 'phone', 'email', 'capacity', 'opening_time', 'closing_time', 'user_password']
#
#
#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         representation['create_at'] = instance.create_at.strftime("%Y-%m-%d %H:%M:%S")
#         representation['update_at'] = instance.update_at.strftime("%Y-%m-%d %H:%M:%S")
#         representation['logo'] = instance.get_logo()
#         return representation
#
#     def create(self, validated_data):
#         user_password = validated_data.pop('user_password', None)
#         if not user_password:
#             user_password = validated_data['rnc']  # Usar RNC como contraseña si no se proporciona una
#
#         # Crear el restaurante
#         restaurant = Restaurant.objects.create(**validated_data)
#
#         # Crear el usuario asociado
#         # username = slugify()  # Convertir el nombre del restaurante en un username válido
#         user = CustomerUser.objects.create(
#             username=validated_data['name'],
#             email=validated_data['email'],
#             phone=validated_data['phone'],
#             password=make_password(user_password)  # Encriptar la contraseña
#         )
#
#         # Asignar el grupo 'restaurant' al usuario
#         restaurant_group, _ = Group.objects.get_or_create(name='restaurant')
#         user.groups.add(restaurant_group)
#
#         return restaurant

class TableSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.CharField(source='restaurant.name', read_only=True)
    restaurant  = serializers.PrimaryKeyRelatedField(
        queryset=Restaurant.objects.all(),
        write_only=True
    )
    restaurant_id = serializers.IntegerField(source='restaurant.id', read_only=True)

    class Meta:
        model = Table
        fields = ['id', 'restaurant','restaurant_id', 'restaurant_name', 'number', 'capacity', 'location', 'status']
        validators = [
            UniqueTogetherValidator(
                queryset=Table.objects.all(),
                fields=['restaurant', 'number'],
                message=_("Ya existe una mesa con este número en este restaurante.")
            )
        ]


    def create(self, validated_data):
        return Table.objects.create(**validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['restaurant_id'] = instance.restaurant.id
        return representation


class TableSummarySerializer(serializers.Serializer):
    restaurant_id = serializers.IntegerField(source='restaurant.id', read_only=True)
    restaurant_name = serializers.CharField(source='restaurant.name', read_only=True)
    summary = serializers.DictField(child=serializers.IntegerField())

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if 'summary' in representation and representation['summary'] is None:
            representation['summary'] = {}
        return representation
