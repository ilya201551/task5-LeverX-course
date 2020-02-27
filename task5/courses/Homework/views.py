from ..models import Homework
from ..permissions import IsProfessorOrReadOnly
from ..Homework.serializers import HomeworkSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


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
