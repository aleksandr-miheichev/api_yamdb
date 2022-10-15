from random import randint, seed

from django.core.mail import send_mail
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.mixins import CreateDestroyListViewSet
from api.permissions import IsStaffOrReadOnly
from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    GetTitleSerializer,
    TitleSerializer
)
from reviews.models import Category, CustomUser, Genre, Title
from reviews.serializers import UsersSerializer


def generate_code():
    seed()
    return str(randint(100000, 999999))


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@api_view(['POST'])
def api_signup(request):
    if request.method == 'POST':
        code = generate_code()
        data = request.data
        data['conformation_code'] = code
        serializer = UsersSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            send_mail(
                'conformation_code',
                f'Here is the confirmation code {code}',
                'from@example.com',
                [request.data['email']],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def api_token(request):
    if (
            request.method == 'POST' and CustomUser.objects.filter(
                username=request.username,
                conformation_code=request.conformation_code
            )):
        return Response(
            get_tokens_for_user(request.username), status=status.HTTP_200_OK
        )
    return Response(status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(CreateDestroyListViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsStaffOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ("name",)


class GenreViewSet(CreateDestroyListViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsStaffOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ("name",)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg('review__score'))
    serializer_class = GetTitleSerializer
    permission_classes = (IsStaffOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'category__slug', 'genre__slug', 'year')

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return GetTitleSerializer
        return TitleSerializer
