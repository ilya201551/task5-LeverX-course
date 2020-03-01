from ..models import (Comment,
                      Mark,
                      )
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


class CommentSerializer(serializers.ModelSerializer):

    def validate_mark(self, value):
        request = self.context['request']
        if value in Mark.objects.filter(solution__owner=request.user):
            return value
        elif value in Mark.objects.filter(solution__homework__lecture__course__professors=request.user):
            return value
        else:
            raise serializers.ValidationError("You cannot add a comment to this mark.")

    def create(self, validated_data):
        request = self.context['request']
        validated_data['owner'] = request.user
        return super().create(validated_data)

    class Meta:
        validators = [UniqueTogetherValidator(queryset=Comment.objects.all(),
                                              fields=['text', 'mark'],
                                              message='This mark already has this comment.'
                                              )
                      ]
        model = Comment
        fields = ['id',
                  'owner',
                  'text',
                  'mark',
                  ]
        read_only_fields = ['owner']
