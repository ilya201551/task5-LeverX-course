from ..models import Solution
from ..permissions import (IsStudentOrReadOnly,
                           IsOwnerOrReadOnly,
                           )
from ..Solutions.serializers import (SolutionSerializer,
                                     SolutionDetailSerializer,
                                     )
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_description="Getting information about all the solutions that the user is related to."))
@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_description="Adding a new solution."))
class SolutionListView(generics.ListCreateAPIView):

    permission_classes = [IsAuthenticated,
                          IsStudentOrReadOnly,
                          ]
    serializer_class = SolutionSerializer

    def get_queryset(self):
        user = self.request.user
        if user.status == 'P':
            queryset = Solution.objects.filter(homework__lecture__course__professors=user).filter(finished=True)
        else:
            queryset = Solution.objects.filter(owner=user)
        return queryset


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_description="Detailed information about the selected solution."))
@method_decorator(name='put', decorator=swagger_auto_schema(
    operation_description="Updating all information about the solution."))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    operation_description="Selectively updating information about a solution."))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    operation_description="Deleting a solution."))
class SolutionDetailView(generics.RetrieveUpdateDestroyAPIView):

        permission_classes = [IsAuthenticated,
                              IsOwnerOrReadOnly,
                              ]
        serializer_class = SolutionDetailSerializer

        def get_queryset(self):
            user = self.request.user
            if user.status == 'P':
                queryset = Solution.objects.filter(homework__lecture__course__professors=user).filter(finished=True)
            else:
                queryset = Solution.objects.filter(owner=user)
            return queryset
