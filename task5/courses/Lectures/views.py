from ..models import Lecture
from ..permissions import (IsOwnerOrReadOnly,
                           IsProfessorOrReadOnly,
                           )
from ..Lectures.serializers import (LecturesListSerializer,
                                    LecturesDetailSerializer,
                                    )
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_description="Getting information about all the lectures that the user is related to."))
@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_description="Adding a new lecture."))
class LecturesListView(generics.ListCreateAPIView):

    permission_classes = [IsAuthenticated,
                          IsProfessorOrReadOnly,
                          ]
    serializer_class = LecturesListSerializer

    def get_queryset(self):
        user = self.request.user
        if user.status == 'P':
            queryset = Lecture.objects.filter(course__professors=user)
        else:
            queryset = Lecture.objects.filter(course__students=user)
        return queryset


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_description="Detailed information about the selected lecture."))
@method_decorator(name='put', decorator=swagger_auto_schema(
    operation_description="Updating all information about the lecture."))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    operation_description="Selectively updating information about a lecture."))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    operation_description="Deleting a lecture."))
class LecturesDetailView(generics.RetrieveUpdateDestroyAPIView):

        permission_classes = [IsAuthenticated,
                              IsOwnerOrReadOnly,
                              ]
        serializer_class = LecturesDetailSerializer

        def get_queryset(self):
            user = self.request.user
            if user.status == 'P':
                queryset = Lecture.objects.filter(course__professors=user)
            else:
                queryset = Lecture.objects.filter(course__students=user)
            return queryset
