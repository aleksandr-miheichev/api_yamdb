from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (api_signup, api_token, CategoryViewSet, GenreViewSet,
                       TitleViewSet)

router_api_v1 = DefaultRouter()

router_api_v1.register('categories', CategoryViewSet, basename='categories')
router_api_v1.register('genres', GenreViewSet, basename='genres')
router_api_v1.register('titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('v1/auth/signup/', api_signup, name='signup'),
    path('v1/auth/token/', api_token, name='token'),
    path('v1/', include(router_api_v1.urls)),
]
