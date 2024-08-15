from django.contrib.auth.models import Group
from rest_framework import serializers
from core.customers.models import *
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomerUser.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomerUser
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name', 'phone']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': "Passwords fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = CustomerUser(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone=validated_data['phone']
        )

        user.set_password(validated_data['password'])
        user.save()

        customer_group, created = Group.objects.get_or_create(name='customer')
        user.groups.add(customer_group)

        return user


class UserProfileSerializer(serializers.ModelSerializer):

        class Meta:
            model = CustomerUser
            fields = ['username', 'email', 'first_name', 'last_name', 'phone']