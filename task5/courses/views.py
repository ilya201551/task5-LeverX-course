from .models import (AdvUser,
                     Course)
from .serializers import (UserRegistrationSerializer,
                          UserSerializer,
                          CoursesListSerializer,
                          CoursesDetailSerializer,
                          CoursesStudentsListSerializer,
                          CoursesProfessorsListSerializer,
                          )
from .permissions import (IsOwnerOrReadOnly,
                          IsProfessorOrReadOnly,
                          )
from rest_framework import (generics,
                            status,
                            )
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


""""Users views"""


class UserRegistrationView(generics.CreateAPIView):

    serializer_class = UserRegistrationSerializer


class UserListView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]
    queryset = AdvUser.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveUpdateAPIView):

    permission_classes = [IsAuthenticated,
                          IsOwnerOrReadOnly,]
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


class CoursesListView(generics.ListCreateAPIView):

    permission_classes = [IsAuthenticated,
                          IsProfessorOrReadOnly]
    serializer_class = CoursesListSerializer

    def get_queryset(self):
        user = self.request.user
        if user.status == 'P':
            queryset = Course.objects.filter(professors=user)
        else:
            queryset = Course.objects.filter(students=user)
        return queryset


class CoursesDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated,
                          IsOwnerOrReadOnly]
    serializer_class = CoursesDetailSerializer

    def get_queryset(self):
        user = self.request.user
        if user.status == 'P':
            queryset = Course.objects.filter(professors=user)
        else:
            queryset = Course.objects.filter(students=user)
        return queryset


class CoursesStudentsListView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CoursesStudentsListSerializer

    def get_queryset(self):
        user = self.request.user
        if user.status == 'P':
            queryset = Course.objects.filter(professors=user)
        else:
            queryset = Course.objects.filter(students=user)
        return queryset


class CoursesProfessorsListView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CoursesProfessorsListSerializer

    def get_queryset(self):
        user = self.request.user
        if user.status == 'P':
            queryset = Course.objects.filter(professors=user)
        else:
            queryset = Course.objects.filter(students=user)
        return queryset


