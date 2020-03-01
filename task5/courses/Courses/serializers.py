from ..models import Course
from ..Users.serializers import UserSerializer
from ..Lectures.serializers import LecturesListSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class CoursesSerializer(serializers.ModelSerializer):

    name = serializers.CharField(min_length=5, max_length=100, validators=[UniqueValidator(
        queryset=Course.objects.all(),
        message='Course already exist.'
    )])
    lectures = serializers.StringRelatedField(many=True, read_only=True)

    def create(self, validated_data):
        request = self.context['request']
        validated_data['owner'] = request.user
        if request.user not in validated_data['professors']:
            validated_data['professors'].append(request.user)
        return super().create(validated_data)

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
        read_only_fields = ['owner']


class CoursesStudentsListSerializer(serializers.ModelSerializer):

    students = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['students']


class CoursesProfessorsListSerializer(serializers.ModelSerializer):

    professors = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['professors']


class CoursesLecturesListSerializer(serializers.ModelSerializer):

    lectures = LecturesListSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['lectures']
