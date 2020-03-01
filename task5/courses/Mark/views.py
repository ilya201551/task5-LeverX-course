from ..models import Mark
from ..permissions import IsProfessorOrReadOnly
from ..Mark.serializers import (MarkSerializer,
                                MarkDetailSerializer,
                                )
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


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
