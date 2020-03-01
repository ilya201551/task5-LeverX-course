from ..models import (Lecture,
                      Course,
                      )
from ..Homework.serializers import HomeworkSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


class LecturesListSerializer(serializers.ModelSerializer):

    tasks = serializers.StringRelatedField(many=True, read_only=True)

    def validate_course(self, value):
        request = self.context['request']
        if value in Course.objects.filter(professors=request.user):
            return value
        else:
            raise serializers.ValidationError("You are not a Professor in this course.")

    def create(self, validated_data):
        request = self.context['request']
        validated_data['owner'] = request.user
        return super().create(validated_data)

    class Meta:
        validators = [UniqueTogetherValidator(queryset=Lecture.objects.all(),
                                              fields=['topic', 'course'],
                                              message='This course already has a lecture with this topic.'
                                              )
                      ]
        model = Lecture
        fields = ['id',
                  'owner',
                  'topic',
                  'presentation',
                  'tasks',
                  'course',
                  ]
        read_only_fields = ['owner', 'tasks']


class LecturesDetailSerializer(serializers.ModelSerializer):

    tasks = HomeworkSerializer(many=True, read_only=True)

    def validate_course(self, value):
        request = self.context['request']
        if value in Course.objects.filter(professors=request.user):
            return value
        else:
            raise serializers.ValidationError("You are not a Professor in this course.")

    class Meta:
        validators = [UniqueTogetherValidator(queryset=Lecture.objects.all(),
                                              fields=['topic', 'course'],
                                              message='This course already has a lecture with this topic.'
                                              )
                      ]
        model = Lecture
        fields = ['id',
                  'owner',
                  'topic',
                  'presentation',
                  'tasks',
                  'course',
                  ]
        read_only_fields = ['owner', 'tasks']
