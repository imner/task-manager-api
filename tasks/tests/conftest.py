import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.fixture
def api_client():
    """Cliente API para hacer requests"""

    return APIClient()

@pytest.fixture
def create_user(db):
    """Fixture para crear usuarios de prueba"""

    def make_user(username="testuser", email="test@example.com", password="TestPass123!", **kwargs):
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            **kwargs
        )
        return user
    return make_user

@pytest.fixture
def user(create_user):
    """Usuario básico para tests"""

    return create_user()

@pytest.fixture
def another_user(create_user):
    """Segundo usuario para tests de permisos"""

    return create_user(
        username="anotheruser",
        email="another@examplecom"
    )

@pytest.fixture
def auth_client(api_client, user):
    """Cliente autenticado con JWT token"""

    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    return api_client

@pytest.fixture
def user_data():
    """Datos válidos para crear un usuario"""

    return {
        "username": "newuser",
        "email": "new@example.com",
        "password": "NewPass123!",
        "password2": "NewPass123!",
        "first_name": "New",
        "last_name": "User"
    }

@pytest.fixture
def login_data():
    """Datos válidos para login"""

    return {
        "username": "testuser",
        "password": "TestPass123!"
    }