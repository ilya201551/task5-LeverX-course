from ..models import Lecture
from ..Homework.serializers import HomeworkSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


class LecturesListSerializer(serializers.ModelSerializer):

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    tasks = serializers.StringRelatedField(many=True, read_only=True)

    def validate_course(self, value):
        request = self.context['request']
        if value in Lecture.objects.filter(course__professors=request.user):
            return value
        else:
            raise serializers.ValidationError("You are not a Professor in this course.")

    class Meta:
        validators = [UniqueTogetherValidator(queryset=Lecture.objects.all(),
                                              fields=['topic', 'course'],
                                              message='This course already has a lecture with this name.'
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


class LecturesDetailSerializer(serializers.ModelSerializer):

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    tasks = HomeworkSerializer(many=True, read_only=True)

    def validate_course(self, value):
        request = self.context['request']
        if value in Lecture.objects.filter(course__professors=request.user):
            return value
        else:
            raise serializers.ValidationError("You are not a Professor in this course.")

    class Meta:
        validators = [UniqueTogetherValidator(queryset=Lecture.objects.all(),
                                              fields=['topic', 'course'],
                                              message='This course already has a lecture with this name.'
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
