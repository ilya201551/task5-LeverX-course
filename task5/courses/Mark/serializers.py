from ..models import (Mark,
                      Solution)
from ..Comments.serializers import CommentSerializer
from rest_framework import serializers


class MarkSerializer(serializers.ModelSerializer):

    value = serializers.IntegerField(min_value=0, max_value=10)
    comments = serializers.StringRelatedField(many=True, read_only=True)

    def validate_solution(self, value):
        request = self.context['request']
        if value in Solution.objects.filter(homework__lecture__course__professors=request.user):
            return value
        else:
            raise serializers.ValidationError("You cannot add a mark to a solution that you are not a Professor of.")

    def create(self, validated_data):
        request = self.context['request']
        validated_data['owner'] = request.user
        return super().create(validated_data)

    class Meta:
        model = Mark
        fields = ['id',
                  'owner',
                  'value',
                  'solution',
                  'comments',
                  ]
        read_only_fields = ['owner',
                            'comments',
                            ]


class MarkDetailSerializer(serializers.ModelSerializer):

    value = serializers.IntegerField(min_value=0, max_value=10)
    comments = CommentSerializer(many=True, read_only=True)

    def validate_solution(self, value):
        request = self.context['request']
        if value in Solution.objects.filter(homework__lecture__course__professors=request.user):
            return value
        else:
            raise serializers.ValidationError("You cannot add a mark to a solution that you are not a Professor of.")

    def create(self, validated_data):
        request = self.context['request']
        validated_data['owner'] = request.user
        return super().create(validated_data)

    class Meta:
        model = Mark
        fields = ['id',
                  'owner',
                  'value',
                  'solution',
                  'comments',
                  ]
        read_only_fields = ['owner',
                            'comments'
                            ]
