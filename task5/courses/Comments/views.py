from ..models import Comment
from ..permissions import IsOwnerOrReadOnly
from ..Comments.serializers import CommentSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_description="Receive a list of comments for all grades they are related to."))
@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_description="Adding a new comment."))
class CommentListView(generics.ListCreateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        user = self.request.user
        if user.status == 'P':
            queryset = Comment.objects.filter(mark__solution__homework__lecture__course__professors=user)
        else:
            queryset = Comment.objects.filter(mark__solution__owner=user)
        return queryset


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_description="Detailed information about the selected comment."))
@method_decorator(name='put', decorator=swagger_auto_schema(
    operation_description="Updating all information about the comment."))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    operation_description="Selectively updating information about a comment."))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    operation_description="Deleting a comment."))
class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):

        permission_classes = [IsAuthenticated,
                              IsOwnerOrReadOnly,
                              ]
        serializer_class = CommentSerializer

        def get_queryset(self):
            user = self.request.user
            if user.status == 'P':
                queryset = Comment.objects.filter(mark__solution__homework__lecture__course__professors=user)
            else:
                queryset = Comment.objects.filter(mark__solution__owner=user)
            return queryset
