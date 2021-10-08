from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import *

urlpatterns = [
	path('auth/signup/', registration_API_view),
	path('auth/token/', take_confirmation_code_view),

]
