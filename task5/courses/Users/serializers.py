from ..models import AdvUser
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class UserRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(min_length=5, max_length=20, validators=[UniqueValidator(
        queryset=AdvUser.objects.all(),
        message='User already exist.',
    )])
    email = serializers.CharField(min_length=5, max_length=30, validators=[UniqueValidator(
        queryset=AdvUser.objects.all(),
        message='Email already exist.',
    )])
    password = serializers.CharField(min_length=8, max_length=25)

    def create(self, validated_data):
        return AdvUser.objects.create_user(**validated_data)

    class Meta:
        model = AdvUser
        fields = ['id',
                  'username',
                  'password',
                  'email',
                  'first_name',
                  'last_name',
                  'status',
                  ]


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdvUser
        fields = ['id',
                  'username',
                  'email',
                  'first_name',
                  'last_name',
                  'status',
                  ]
