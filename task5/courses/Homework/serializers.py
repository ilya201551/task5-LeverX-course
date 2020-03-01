from ..models import (Homework,
                      Lecture,
                      )
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


class HomeworkSerializer(serializers.ModelSerializer):

    task = serializers.CharField(min_length=5, max_length=1000)

    def validate_lecture(self, value):
        request = self.context['request']
        if value in Lecture.objects.filter(course__professors=request.user):
            return value
        else:
            raise serializers.ValidationError("You cannot add a task to a lecture that you are not a Professor of.")

    def create(self, validated_data):
        request = self.context['request']
        validated_data['owner'] = request.user
        return super().create(validated_data)

    class Meta:
        validators = [UniqueTogetherValidator(queryset=Homework.objects.all(),
                                              fields=['task', 'lecture'],
                                              message='This lecture already has this task.'
                                              )
                      ]
        model = Homework
        fields = ['id',
                  'owner',
                  'task',
                  'lecture',
                  ]
        read_only_fields = ['owner']
