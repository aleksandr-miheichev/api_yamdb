from random import randint, seed
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.serializers import UsersSerializer
from reviews.models import CustomUser


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
        )
    ):
        return Response(
            get_tokens_for_user(request.username), status=status.HTTP_200_OK
        )
    return Response(status=status.HTTP_400_BAD_REQUEST)
