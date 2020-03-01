from ..models import (Mark,
                      Solution)
from rest_framework import serializers


class MarkSerializer(serializers.ModelSerializer):

    value = serializers.IntegerField(min_value=0, max_value=10)

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
                  ]
        read_only_fields = ['owner']
