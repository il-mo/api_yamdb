from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    take_confirmation_code_view,
    registration_API_view,
    UserViewSet)

router = DefaultRouter()

router.register(
    'users', UserViewSet, basename='users'
)
urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', registration_API_view),
    path('auth/token/', take_confirmation_code_view),
]
