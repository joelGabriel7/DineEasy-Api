from datetime import datetime

from rest_framework import serializers

from core.reservations.models import Reservation


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

