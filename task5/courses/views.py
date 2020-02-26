from .models import (AdvUser,
                     Course,
                     Lecture,
                     Homework,
                     )
from .serializers import (UserRegistrationSerializer,
                          UserSerializer,
                          CoursesSerializer,
                          CoursesStudentsListSerializer,
                          CoursesProfessorsListSerializer,
                          CoursesLecturesListSerializer,
                          LecturesListSerializer,
                          LecturesDetailSerializer,
                          HomeworkSerializer,
                          )
from .permissions import (IsOwnerOrReadOnly,
                          IsThisUserOrReadOnly,
                          IsProfessorOrReadOnly,
                          )
from rest_framework import (generics,
                            status,
                            viewsets,
                            parsers,
                            )
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action


""""Users views"""


class UserRegistrationView(generics.CreateAPIView):

    serializer_class = UserRegistrationSerializer


class UserViewSet(viewsets.ModelViewSet):

    def get_permissions(self):
        if self.action == 'list' or self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated,
                                  IsThisUserOrReadOnly,
                                  ]
        return [permission() for permission in permission_classes]
    queryset = AdvUser.objects.all()
    serializer_class = UserSerializer


class UserLoginView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'email': user.email,
        },
            status=status.HTTP_200_OK,
        )


class UserLogoutView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


"""Courses views"""


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


"""Lectures views"""


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


"""Homework views"""


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
