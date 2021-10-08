from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, ReviewViewSet, CategoryViewSet, GenreViewSet, TitleViewSet

router = DefaultRouter()

router.register(
    r'titles',
    TitleViewSet,
    basename='TitleView'
)
router.register(
    'genres',
    GenreViewSet,
    basename='GenreView'
)
router.register(
    'categories',
    CategoryViewSet,
    basename='CategoryView'
)

router.register(
    r'v1/titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
router.register(
    r'v1/titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments', CommentViewSet, basename='reviews'
)

urlpatterns = [
	path('', include(router.urls)),
	path('v1/', include('users.urls'))
]
