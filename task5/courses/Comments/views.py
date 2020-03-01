from ..models import Comment
from ..permissions import IsOwnerOrReadOnly
from ..Comments.serializers import CommentSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


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
