from ..models import AdvUser
from ..permissions import IsThisUserOrReadOnly
from ..Users.serializers import (UserSerializer,
                                 UserRegistrationSerializer
                                 )
from rest_framework import (generics,
                            status,
                            viewsets,
                            )
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_description="Register a new user."))
class UserRegistrationView(generics.CreateAPIView):

    serializer_class = UserRegistrationSerializer


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description="Getting information about all the users."))
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_description="Register a new user."))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_description="Detailed information about the selected user."))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_description="Updating all information about the user."))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    operation_description="Selectively updating information about a user."))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_description="Deleting a user."))
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

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        else:
            return UserSerializer


class UserLoginView(ObtainAuthToken):

    @swagger_auto_schema(operation_description="Login.")
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

    @swagger_auto_schema(operation_description="Logout.")
    def get(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
