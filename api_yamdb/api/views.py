from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .filters import TitlesFilter
from rest_framework.filters import SearchFilter
from reviews.models import Comment, Review, Titles, Category, Genre
from rest_framework import filters, mixins, permissions, viewsets
# from rest_framework.pagination import LimitOffsetPagination
# from django_filters.rest_framework import DjangoFilterBackend
#
# from .permissions import IsAuthorOrReadOnlyPermission
from .serializers import (
    ReviewSerializer,
    CommentSerializer,
    CategorySerializer,
    GenreSerializer,
    TitleGetSerializer,
    TitlePostSerializer
)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    #permission_classes = [permissions.IsAuthenticated]

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


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.annotate(
        rating=Avg('reviews__score')).order_by('name')
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year',)
    filterset_class = TitlesFilter
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly, isAdminOrReadOnly)
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TitleGetSerializer
        return TitlePostSerializer


class CategoryAndGenreViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)
    lookup_field = 'slug'
    search_fields = ['name']
    filter_backends = [SearchFilter]
    pagination_class = PageNumberPagination


class CategoryViewSet(CategoryAndGenreViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryAndGenreViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
