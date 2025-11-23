from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserSerializer,
    UserProfileUpdateSerializer
)

# Create your views here.

class RegistrationAPIView(APIView):
    """
        Vista para registro de nuevos usuarios
        POST /api/auth/register/
    """

    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "user": UserSerializer(user).data,
            "message": "Usuario registrado exitosamente",
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }
        }, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    """
        Vista para login de usuarios
        POST /api/auth/login/
    """
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        user = authenticate(username=username, password=password)

        if user is None:
            return Response({
                "error": "Credenciales inválidas"
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        if not user.is_active:
            return Response({
                "error": "Usuario inactivo"
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        refresh = RefreshToken.for_user(user)

        return Response({
            "user": UserSerializer(user).data,
            "message": "Login exitoso",
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }
        }, status=status.HTTP_200_OK)


class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    """
        Vista para obtener y actualizar el perfil del usuario autenticado
        GET /api/auth/profile/
        PUT /api/auth/profile/
        PATCH /api/auth/profile/
    """

    serializer_class = UserProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        return Response({
            "user": UserSerializer(request.user).data,
            "profile": serializer.data
        }, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    """
        Vista para logout (blacklist del refresh token)
        POST /api/auth/logout/
    """
    
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.get("refresh_token")
            if not refresh_token:
                return Response({
                    "error": "Se requiere el refresh token"

                }, status=status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response({
                "message": "Logout exitoso"
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response ({
                "error": "Token inválido o expirado"
            }, status=status.HTTP_400_BAD_REQUEST)
