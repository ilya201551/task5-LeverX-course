from .serializers import (CoursesSerializer,
                          CoursesLecturesListSerializer,
                          CoursesProfessorsListSerializer,
                          CoursesStudentsListSerializer,
                          )
from ..models import Course
from ..permissions import (IsOwnerOrReadOnly,
                           IsProfessorOrReadOnly,
                           )
from rest_framework import (viewsets,
                            status,
                            )
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description="Getting information about all the courses that the user is related to."))
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_description="Adding a new course."))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_description="Detailed information about the selected course."))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_description="Updating all information about the course."))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    operation_description="Selectively updating information about a course."))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_description="Deleting a course."))
@method_decorator(name='students', decorator=swagger_auto_schema(
    operation_description="List of students in the selected course."))
@method_decorator(name='professors', decorator=swagger_auto_schema(
    operation_description="List of professors in the selected course."))
@method_decorator(name='lectures', decorator=swagger_auto_schema(
    operation_description="List of lectures in the selected course."))
class CoursesViewSet(viewsets.ModelViewSet):

    def get_permissions(self):
        if self.action == 'list' or self.action == 'create' or self.action == 'retrieve':
            permission_classes = [IsAuthenticated,
                                  IsProfessorOrReadOnly,
                                  ]
        else:
            permission_classes = [IsAuthenticated,
                                  IsOwnerOrReadOnly,
                                  ]
        return [permission() for permission in permission_classes]

    serializer_class = CoursesSerializer

    def get_queryset(self):
        user = self.request.user
        if user.status == 'P':
            queryset = Course.objects.filter(professors=user)
        else:
            queryset = Course.objects.filter(students=user)
        return queryset

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def students(self, request, pk=None):
        data = Course.objects.get(pk=pk)
        serializer = CoursesStudentsListSerializer(data)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def professors(self, request, pk=None):
        data = Course.objects.get(pk=pk)
        serializer = CoursesProfessorsListSerializer(data)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def lectures(self, request, pk=None):
        data = Course.objects.get(pk=pk)
        serializer = CoursesLecturesListSerializer(data)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)
