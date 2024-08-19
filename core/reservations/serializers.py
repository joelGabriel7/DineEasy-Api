from datetime import datetime

from rest_framework import serializers

from core.reservations.models import Reservation
from core.restaurant.models import Restaurant


class ReservationSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.CharField(source='restaurant.name', read_only=True)
    time = serializers.TimeField(format='%I:%M %p', input_formats=['%I:%M %p', '%H:%M'])

    class Meta:
        model = Reservation
        fields = ['id', 'customer', 'restaurant', 'restaurant_name', 'date', 'time', 'party_size', 'special_request',
                  'status']
        extra_kwargs = {
            'special_request': {'required': False}
        }


class ResevationsByRestaurantsSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.CharField(source='restaurant.name', read_only=True)
    restaurant = serializers.PrimaryKeyRelatedField(
        queryset=Restaurant.objects.all(),
        write_only=True
    )
    restaurant_id = serializers.IntegerField(source='restaurant.id', read_only=True)

    class Meta:
        model = Reservation
        fields = ['id', 'customer', 'restaurant', 'restaurant_id', 'restaurant_name', 'date', 'time', 'party_size',
                  'special_request',
                  'status']
