from ..models import (Solution,
                      Homework,
                      )
from ..Mark.serializers import MarkSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


class SolutionSerializer(serializers.ModelSerializer):

    link = serializers.CharField(min_length=5, max_length=100)
    mark = serializers.StringRelatedField(many=False, read_only=True)

    def validate_homework(self, value):
        request = self.context['request']
        if value in Homework.objects.filter(lecture__course__students=request.user):
            return value
        else:
            raise serializers.ValidationError("You cannot add a solution to a course that you are not a Student of.")

    def create(self, validated_data):
        request = self.context['request']
        validated_data['owner'] = request.user
        return super().create(validated_data)

    class Meta:
        validators = [UniqueTogetherValidator(queryset=Solution.objects.all(),
                                              fields=['link', 'homework'],
                                              message='This homework already has this solution.'
                                              )
                      ]
        model = Solution
        fields = ['id',
                  'owner',
                  'link',
                  'mark',
                  'finished',
                  'homework'
                  ]
        read_only_fields = ['owner']


class SolutionDetailSerializer(serializers.ModelSerializer):

    link = serializers.CharField(min_length=5, max_length=100)
    mark = MarkSerializer(many=False, read_only=True)

    def validate_homework(self, value):
        request = self.context['request']
        if value in Homework.objects.filter(lecture__course__students=request.user):
            return value
        else:
            raise serializers.ValidationError("You cannot add a solution to a course that you are not a Student of.")

    class Meta:
        validators = [UniqueTogetherValidator(queryset=Solution.objects.all(),
                                              fields=['link', 'homework'],
                                              message='This homework already has this solution.'
                                              )
                      ]
        model = Solution
        fields = ['id',
                  'owner',
                  'link',
                  'mark',
                  'finished',
                  'homework'
                  ]
        read_only_fields = ['owner']
