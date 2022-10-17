from random import randint, seed

from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

from api.filters import TitleFilter
from api.mixins import CreateDestroyListViewSet
from api.permissions import IsAdminOnly, IsStaffOrReadOnly, IfAdminModeratorAuthorPermission
from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    GetTitleSerializer,
    TitleSerializer,
    ReviewSerializer,
    CommentSerializer
)
from api_yamdb.settings import DEFAULT_FROM_EMAIL
from reviews.models import Category, CustomUser, Genre, Title, Comment, Review
from reviews.serializers import (
    AdminSerializer,
    MeSerializer,
    SignUpSerializer,
    TokenSerializer
)


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
    code = generate_code()
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        user, created = CustomUser.objects.get_or_create(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email'],
        )
        user.set_password(code)
        user.save()
        send_mail_code(code, user.email)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(
        serializer.errors, status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def api_token(request):
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        user = get_object_or_404(
            CustomUser,
            username=serializer.validated_data['username'],
            password=serializer.validated_data['confirmation_code'],
        )
        return Response(
            get_tokens_for_user(user),
            status=status.HTTP_200_OK
        )
    return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class AdminViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = CustomUser.objects.all()
    serializer_class = AdminSerializer
    permission_classes = [IsAdminOnly]
    filter_backends = [SearchFilter]
    search_fields = ('=username',)


@api_view(['POST', 'GET'])
@permission_classes([IsAdminOnly])
def api_admin_signup(request):
    if request.method == 'POST':
        serializer = AdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    users = CustomUser.objects.all()
    serializer = AdminSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PATCH', 'GET'])
def api_me(request):
    user = get_object_or_404(CustomUser, username=request.user.username)
    if request.method == 'PATCH':
        serializer = MeSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    serializer = MeSerializer(user, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PATCH', 'GET', 'DELETE'])
@permission_classes([IsAdminOnly])
def api_users(request, username):
    user = get_object_or_404(CustomUser, username=username)
    if request.method == 'PATCH':
        serializer = AdminSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        CustomUser.objects.filter(username=username).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    serializer = AdminSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(CreateDestroyListViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsStaffOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CreateDestroyListViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsStaffOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(score=Avg('reviews__score'))
    permission_classes = (IsStaffOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return GetTitleSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IfAdminModeratorAuthorPermission,)

    def get_queryset(self):
        review = get_object_or_404(
            Title,
            pk=self.kwargs.get('title_id'))
        return review.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IfAdminModeratorAuthorPermission,)

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
