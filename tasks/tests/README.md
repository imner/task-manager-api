# Tests del Sistema de Autenticación

## Estructura de Tests

### test_auth.py
Tests completos del sistema de autenticación.

#### TestUserRegistration
- ✅ Registro exitoso de usuario
- ✅ Validación de username único
- ✅ Validación de email único
- ✅ Validación de contraseñas coincidentes
- ✅ Validación de contraseña fuerte
- ✅ Validación de campos requeridos
- ✅ Creación automática de perfil

#### TestUserLogin
- ✅ Login exitoso
- ✅ Login con contraseña incorrecta
- ✅ Login con usuario inexistente
- ✅ Login sin credenciales
- ✅ Login con usuario inactivo

#### TestUserProfile
- ✅ Obtener perfil autenticado
- ✅ Bloqueo sin autenticación
- ✅ Actualizar perfil completo
- ✅ Actualizar email
- ✅ Actualización parcial

#### TestTokenRefresh
- ✅ Refresh token válido
- ✅ Refresh token inválido

#### TestLogout
- ✅ Logout exitoso
- ✅ Logout sin token
- ✅ Logout sin autenticación

#### TestUserPermissions
- ✅ Aislamiento entre usuarios

## Ejecutar Tests
```bash
# Todos los tests
pytest

# Solo autenticación
pytest tasks/tests/test_auth.py -v

# Con coverage
pytest --cov=tasks

# Test específico
pytest tasks/tests/test_auth.py::TestUserLogin::test_login_success -v
```

## Coverage Objetivo

- **Líneas:** > 90%
- **Funciones:** 100%
- **Branches:** > 85%
