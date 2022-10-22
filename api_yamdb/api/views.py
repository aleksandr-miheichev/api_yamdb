from random import randint, seed

from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from api.filters import TitleFilter
from api.permissions import (IfAdminModeratorAuthorPermission, IsAdminOnly,
                             IsStaffOrReadOnly)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, GetTitleSerializer,
                             ReviewSerializer, SignUpSerializer,
                             TitleSerializer, TokenSerializer, UsersSerializer)
from api_yamdb.settings import DEFAULT_FROM_EMAIL
from reviews.models import Category, CustomUser, Genre, Review, Title


def generate_code():
    seed()
    return str(randint(100000, 999999))


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {"token": str(refresh.access_token)}


def send_mail_code(code, email):
    send_mail(
        'confirmation_code',
        f'Here is confirmation_code {code}',
        DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def api_signup(request):
    serializer = SignUpSerializer(data=request.data)
    try:
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
    except ValidationError:
        username = serializer.data['username']
        email = serializer.data['email']
    user, created = CustomUser.objects.get_or_create(
        username=username,
        email=email,
    )
    code = generate_code()
    user.confirmation_code = code
    user.save()
    send_mail_code(code, user.email)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def api_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        CustomUser,
        username=serializer.validated_data['username'],
        confirmation_code=serializer.validated_data['confirmation_code'],
    )
    return Response(
        get_tokens_for_user(user),
        status=status.HTTP_200_OK
    )


class UsersViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAdminOnly]
    filter_backends = [SearchFilter]
    search_fields = ('=username',)
    lookup_field = 'username'

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        if request.method == 'GET':
            return Response(
                self.get_serializer(request.user).data,
                status=status.HTTP_200_OK
            )
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AbstractViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """Абстрактный вьюсет для вьюсетов Категория и Жанр."""
    permission_classes = (IsStaffOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(AbstractViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(AbstractViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    permission_classes = (IsStaffOrReadOnly,)
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filterset_class = TitleFilter
    ordering_fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                       'category')
    ordering = ('name',)

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return GetTitleSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IfAdminModeratorAuthorPermission,)

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IfAdminModeratorAuthorPermission,)

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
