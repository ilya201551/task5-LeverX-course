from ..models import Lecture
from ..permissions import (IsOwnerOrReadOnly,
                           IsProfessorOrReadOnly,
                           )
from ..Lectures.serializers import (LecturesListSerializer,
                                    LecturesDetailSerializer,
                                    )
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


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
