from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer para el perfil de usuario"""

    class Meta:
        model = UserProfile
        fields = ["bio", "location", "birth_date", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]


class UserSerializer(serializers.ModelSerializer):
    """Serializer básico para el modelo User"""

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]
        read_only_fields = ["id", "date_joined"]


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer para registro de nuevos usuarios"""

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password], style={"input_type": "password"})
    password2 = serializers.CharField(write_only=True, required=True, style={"input_type": "password"})
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "password", "password2", "email", "first_name", "last_name"]
        extra_kwargs = {
            "first_name": {"required": False},
            "last_name": {"required": False},
        }
    
    def validate(self, attrs):
        """Validar que las contraseñas coincidan"""
        
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        return attrs
    
    def validate_email(self, value):
        """Validar que el email sea único"""
        
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email ya está registrado.")
        return value
    
    def create(self, validated_data):
        """Crear un nuevo usuario"""
        
        validated_data.pop("password2")
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer para login de usuarios"""

    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True, style={"input_type": "password"})


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer para actualizar el perfil de usuario"""

    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email")
    first_name = serializers.CharField(source="user.first_name", required=False)
    last_name = serializers.CharField(source="user.last_name", required=False)

    class Meta:
        model = UserProfile
        fields = ["username", "email", "first_name", "last_name", "bio", "location", "birth_date"]

    def update(self, instance, validated_data):
        """Actualizar tanto User como UserProfile"""

        user_data = validated_data.pop("user", {})
        user = instance.user

        # Actualizar datos del User
        user.email = user_data.get("email", user.email)
        user.first_name = user_data.get("first_name", user.first_name)
        user.last_name = user_data.get("last_name", user.last_name)
        user.save()

        # Actualizar datos del UserProfile
        instance.bio = validated_data.get("bio", instance.bio)
        instance.location = validated_data.get("location", instance.location)
        instance.birth_date = validated_data.get("birth_date", instance.birth_date)
        instance.save()
        return instance
