from ..models import Homework
from ..permissions import IsProfessorOrReadOnly
from ..Homework.serializers import HomeworkSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_description="Getting information about all the homework tasks that the user is related to."))
@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_description="Adding a new homework."))
class HomeworkListView(generics.ListCreateAPIView):

    permission_classes = [IsAuthenticated,
                          IsProfessorOrReadOnly,
                          ]
    serializer_class = HomeworkSerializer

    def get_queryset(self):
        user = self.request.user
        if user.status == 'P':
            queryset = Homework.objects.filter(lecture__course__professors=user)
        else:
            queryset = Homework.objects.filter(lecture__course__students=user)
        return queryset


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_description="Detailed information about the selected homework."))
@method_decorator(name='put', decorator=swagger_auto_schema(
    operation_description="Updating all information about the homework."))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    operation_description="Selectively updating information about a homework."))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    operation_description="Deleting a homework."))
class HomeworkDetailView(generics.RetrieveUpdateDestroyAPIView):

        permission_classes = [IsAuthenticated,
                              IsProfessorOrReadOnly,
                              ]
        serializer_class = HomeworkSerializer

        def get_queryset(self):
            user = self.request.user
            if user.status == 'P':
                queryset = Homework.objects.filter(lecture__course__professors=user)
            else:
                queryset = Homework.objects.filter(lecture__course__students=user)
            return queryset
