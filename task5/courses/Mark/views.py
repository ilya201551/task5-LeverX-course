from ..models import Mark
from ..permissions import IsProfessorOrReadOnly
from ..Mark.serializers import (MarkSerializer,
                                MarkDetailSerializer,
                                )
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_description="Getting information about all the marks that the user is related to."))
@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_description="Adding a new mark."))
class MarkListView(generics.ListCreateAPIView):

    permission_classes = [IsAuthenticated,
                          IsProfessorOrReadOnly,
                          ]
    serializer_class = MarkSerializer

    def get_queryset(self):
        user = self.request.user
        if user.status == 'P':
            queryset = Mark.objects.filter(solution__homework__lecture__course__professors=user)
        else:
            queryset = Mark.objects.filter(solution__homework__lecture__course__students=user)
        return queryset


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_description="Detailed information about the selected mark."))
@method_decorator(name='put', decorator=swagger_auto_schema(
    operation_description="Updating all information about the mark."))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    operation_description="Selectively updating information about a mark."))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    operation_description="Deleting a mark."))
class MarkDetailView(generics.RetrieveUpdateDestroyAPIView):

        permission_classes = [IsAuthenticated,
                              IsProfessorOrReadOnly,
                              ]
        serializer_class = MarkDetailSerializer

        def get_queryset(self):
            user = self.request.user
            if user.status == 'P':
                queryset = Mark.objects.filter(solution__homework__lecture__course__professors=user)
            else:
                queryset = Mark.objects.filter(solution__homework__lecture__course__students=user)
            return queryset
