from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (api_me, api_signup, api_token, api_users, AdminViewSet,
                       CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, TitleViewSet)

router_api_v1 = DefaultRouter()

router_api_v1.register('categories', CategoryViewSet, basename='categories')
router_api_v1.register('genres', GenreViewSet, basename='genres')
router_api_v1.register('titles', TitleViewSet, basename='titles')
router_api_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='Reviews'
)
router_api_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='Comments'
)

urlpatterns = [
    path('v1/auth/signup/', api_signup, name='signup'),
    path('v1/auth/token/', api_token, name='token'),
    path(
        'v1/users/',
        AdminViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='admin_signup'
    ),
    path('v1/users/me/', api_me, name='me'),
    path('v1/users/<str:username>/', api_users, name='users'),
    path('v1/', include(router_api_v1.urls)),
]
