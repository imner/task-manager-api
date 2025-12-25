import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

@pytest.mark.django_db
class TestUserRegistration:
    """Tests para el registro de usuarios"""

    def test_register_user_success(self, api_client, user_data):
        """Test: Registro exitoso de un nuevo usuario"""

        url = reverse("register")
        response = api_client.post(url, user_data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert "user" in response.data
        assert "tokens" in response.data
        assert "access" in response.data["tokens"]
        assert "refresh" in response.data["tokens"]
        assert response.data["user"]["username"] == user_data["username"]
        assert response.data["user"]["email"] == user_data["email"]
        assert User.objects.filter(username=user_data["username"]).exists()

    def test_register_user_with_existing_username(self, api_client, user, user_data):
        """Test: No se puede registrar con username existente"""

        user_data["username"] = user.username
        url = reverse("register")
        response = api_client.post(url, user_data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_user_with_existing_email(self, api_client, user, user_data):
        """Test: No se puede registrar con email existente"""

        user_data["email"] = user.email
        url = reverse("register")
        response = api_client.post(url, user_data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.data

    def test_register_user_password_mismatch(self, api_client, user_data):
        """Test: Las contraseñas deben coincidir"""

        user_data["password2"] = "Differentpassword123!"
        url = reverse("register")
        response = api_client.post(url, user_data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        # assert "password" in response.data

    def test_register_user_weak_password(self, api_client, user_data):
        """Test: Contraseña débil debe ser rechazada"""

        user_data["password"] = "123456"
        user_data["password2"]= "123456"
        url = reverse("register")
        response = api_client.post(url, user_data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_user_missing_required_fields(self, api_client):
        """Test: Campos requeridos deben estar presentes"""

        url = reverse("register")
        response = api_client.post(url, {}, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'username' in response.data
        assert 'email' in response.data
        assert 'password' in response.data

    def test_register_user_creates_profile(self, api_client, user_data):
        """Test: El registro debe crear automáticamente un perfil"""

        url = reverse("register")
        response = api_client.post(url, user_data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        user = User.objects.get(username=user_data['username'])
        assert hasattr(user, 'profile')
        assert user.profile is not None