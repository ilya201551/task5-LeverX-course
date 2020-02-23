from .models import (AdvUser,
                     Course,
                     Lecture)
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


"""User serializers"""


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


"""Courses serializers"""


class CoursesListSerializer(serializers.ModelSerializer):

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate(self, data):
        if 'professors' in data.keys():
            for i in data['professors']:
                if i.status != 'P':
                    raise serializers.ValidationError("Only professors can be added.")
        if 'students' in data.keys():
            for i in data['students']:
                if i.status != 'S':
                    raise serializers.ValidationError("Only students can be added.")
        return data

    class Meta:
        model = Course
        fields = ['id',
                  'owner',
                  'name',
                  'students',
                  'professors',
                  ]


class CoursesDetailSerializer(serializers.ModelSerializer):

    lectures = serializers.StringRelatedField(many=True, read_only=True)

    def validate(self, data):
        if 'professors' in data.keys():
            for i in data['professors']:
                if i.status != 'P':
                    raise serializers.ValidationError("Only professors can be added.")
        if 'students' in data.keys():
            for i in data['students']:
                if i.status != 'S':
                    raise serializers.ValidationError("Only students can be added.")
        return data

    class Meta:
        model = Course
        fields = ['id',
                  'owner',
                  'name',
                  'students',
                  'professors',
                  'lectures',
                  ]
