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


class CoursesViewSet(viewsets.ModelViewSet):

    def get_permissions(self):
        if self.action == 'list' or self.action == 'create':
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

    @action(detail=True, methods=['get'])
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
