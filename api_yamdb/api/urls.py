from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet)

router = DefaultRouter()

router.register('v1/titles', TitleViewSet, basename='TitleView')
router.register('v1/genres', GenreViewSet, basename='GenreView')
router.register('v1/categories', CategoryViewSet, basename='CategoryView')

router.register(
    r'v1/titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
router.register(
    r'v1/titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)

urlpatterns = [
    path('', include(router.urls)),
]
