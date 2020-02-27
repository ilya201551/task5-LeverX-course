from ..models import Homework
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


class HomeworkSerializer(serializers.ModelSerializer):

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    task = serializers.CharField(min_length=5, max_length=1000)

    def validate_lecture(self, value):
        request = self.context['request']
        if value in Homework.objects.filter(lecture__course__professors=request.user):
            return value
        else:
            raise serializers.ValidationError("""You cannot add a task to a course lecture
                                              that you are not a Professor of.""")

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
