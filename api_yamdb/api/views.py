from django.shortcuts import get_object_or_404
from reviews.models import Comment, Review, Titles
from rest_framework import filters, mixins, permissions, viewsets
# from rest_framework.pagination import LimitOffsetPagination
# from django_filters.rest_framework import DjangoFilterBackend
#
# from .permissions import IsAuthorOrReadOnlyPermission
from .serializers import (
    ReviewSerializer,
    CommentSerializer,

)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    # permission_classes = [IsAuthorOrReadOnlyPermission]

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        serializer.save(author=self.request.user, review=review)