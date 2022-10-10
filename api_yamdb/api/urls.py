from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import SignUpView

urlpatterns = [
    path('v1/auth/signup/', SignUpView.as_view(), name='signup'),
    path(
        'v1/auth/token/',
        TokenObtainPairView.as_view(),
        name='token'
    ),
    #path('v1/users/<str:username>/', UserViewSet),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
