from django.urls import path, include

from .views import api_signup, api_token

urlpatterns = [
    path('v1/auth/signup/', api_signup, name='signup'),
    path('v1/auth/token/', api_token, name='token'),
    # path('v1/users/<str:username>/', UserViewSet),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
