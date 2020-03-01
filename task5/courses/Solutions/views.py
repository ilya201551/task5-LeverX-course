from ..models import Solution
from ..permissions import (IsStudentOrReadOnly,
                           IsOwnerOrReadOnly,
                           )
from ..Solutions.serializers import (SolutionSerializer,
                                     SolutionDetailSerializer,
                                     )
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


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
