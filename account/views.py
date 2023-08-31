from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from .serializers import (
    RegistrationSerializer, 
    ActivationSerializer, 
    LoginSerializer, 
    ChangePasswordSerializer, 
    LosePasswordSerializer,
    LosePasswordCompleteSerializer
)
from django.contrib.auth import get_user_model
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .permissions import IsActivePermission
from rest_framework.permissions import IsAuthenticated


User = get_user_model()


class RegistrationView(CreateAPIView):
    serializer_class = RegistrationSerializer


class ActivationView(CreateAPIView):
    serializer_class = ActivationSerializer


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer


class LogoutView(APIView):
    permission_classes = [IsActivePermission]

    def post(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response(
            'Вы успешно вышли из своего аккаунта'
        )


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        return Response(
            'Пароль успешно обнавлен', status=200
        )

class LosePasswordView(CreateAPIView):
    serializer_class = LosePasswordSerializer

class LosePasswordCompleteView(CreateAPIView):
    serializer_class = LosePasswordCompleteSerializer
