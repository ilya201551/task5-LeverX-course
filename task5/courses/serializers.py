from .models import (AdvUser,
                     Course,
                     Lecture,
                     Homework,
                     )
from rest_framework import serializers
from rest_framework.validators import (UniqueValidator,
                                       UniqueTogetherValidator,
                                       )


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


"""Homework serializers"""


class HomeworkSerializer(serializers.ModelSerializer):

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    task = serializers.CharField(min_length=5, max_length=1000)

    def validate_lecture(self, value):
        request = self.context['request']
        if value in Lecture.objects.filter(course__professors=request.user):
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


"""Lectures serializers"""


class LecturesListSerializer(serializers.ModelSerializer):

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    tasks = serializers.StringRelatedField(many=True, read_only=True)

    def validate_course(self, value):
        request = self.context['request']
        if value in Course.objects.filter(professors=request.user):
            return value
        else:
            raise serializers.ValidationError("You are not a Professor in this course.")

    class Meta:
        validators = [UniqueTogetherValidator(queryset=Homework.objects.all(),
                                              fields=['task', 'lecture'],
                                              message='This lecture already has such a task.'
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
        if value in Course.objects.filter(professors=request.user):
            return value
        else:
            raise serializers.ValidationError("This lecture already has such a task.")

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


"""Courses serializers"""


class CoursesSerializer(serializers.ModelSerializer):

    name = serializers.CharField(min_length=5, max_length=100, validators=[UniqueValidator(
        queryset=Course.objects.all(),
        message='Course already exist.'
    )])
    lectures = serializers.StringRelatedField(many=True, read_only=True)
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
                  'lectures',
                  ]


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
