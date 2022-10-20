from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (api_me, api_signup, api_token, api_users, AdminViewSet,
                       CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, TitleViewSet)

router_v1 = DefaultRouter()

router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='Reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='Comments'
)

users_urlpatterns = [
    path(
        '',
        AdminViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='admin_signup'
    ),
    path('me/', api_me, name='me'),
    path('<str:username>/', api_users, name='users'),
]

auth_urlpatterns = [
    path('signup/', api_signup, name='signup'),
    path('token/', api_token, name='token'),
]

v_urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include(auth_urlpatterns)),
    path('users/', include(users_urlpatterns)),
]

urlpatterns = [
    path('v1/', include(v_urlpatterns)),
]
