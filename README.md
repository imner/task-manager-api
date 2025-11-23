# 📋 Task Manager API

API REST profesional para gestión de tareas y proyectos, construida con Django REST Framework.

## 🚀 Características

- ✅ Autenticación JWT
- ✅ CRUD completo de tareas
- ✅ Organización por proyectos
- ✅ Filtros y búsquedas avanzadas
- ✅ Documentación automática con Swagger
- ✅ Tests comprehensivos
- ✅ PostgreSQL como base de datos

## 🛠️ Tecnologías

- **Backend:** Django 5.0, Django REST Framework 3.14
- **Base de datos:** PostgreSQL 15
- **Autenticación:** JWT (Simple JWT)
- **Documentación:** drf-spectacular (OpenAPI 3.0)
- **Testing:** pytest, pytest-django

## 📦 Instalación

### Requisitos previos

- Python 3.11+
- PostgreSQL 15+
- pip

### 1. Clonar el repositorio
```bash
git clone https://github.com/imner/task-manager-api.git
cd task-manager-api
```

### 2. Crear entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
```bash
cp .env.example .env
# Editar .env con tus credenciales
```

### 5. Crear base de datos PostgreSQL
```sql
CREATE DATABASE task_manager_db;
CREATE USER task_manager_user WITH PASSWORD 'tu_password';
GRANT ALL PRIVILEGES ON DATABASE task_manager_db TO task_manager_user;
```

### 6. Ejecutar migraciones
```bash
python manage.py migrate
```

### 7. Crear superusuario
```bash
python manage.py createsuperuser
```

### 8. Ejecutar servidor
```bash
python manage.py runserver
```

La API estará disponible en `http://localhost:8000`

## 📚 Documentación API

- **Swagger UI:** http://localhost:8000/api/docs/
- **ReDoc:** http://localhost:8000/api/redoc/
- **Schema JSON:** http://localhost:8000/api/schema/

## 🔐 Endpoints principales

### Autenticación
```
POST   /api/auth/register/     - Registro de usuario
POST   /api/auth/login/        - Login (obtener JWT token)
GET    /api/auth/profile/      - Perfil del usuario
POST   /api/auth/token/refresh/ - Refrescar token
```

### Tareas
```
GET    /api/tasks/             - Listar tareas
POST   /api/tasks/             - Crear tarea
GET    /api/tasks/{id}/        - Detalle de tarea
PUT    /api/tasks/{id}/        - Actualizar tarea
DELETE /api/tasks/{id}/        - Eliminar tarea
GET    /api/tasks/stats/       - Estadísticas de tareas
GET    /api/tasks/overdue/     - Tareas vencidas
```

### Proyectos
```
GET    /api/projects/          - Listar proyectos
POST   /api/projects/          - Crear proyecto
GET    /api/projects/{id}/     - Detalle de proyecto
PUT    /api/projects/{id}/     - Actualizar proyecto
DELETE /api/projects/{id}/     - Eliminar proyecto
```

## 🧪 Testing
```bash
# Ejecutar todos los tests
pytest

# Con coverage
pytest --cov=tasks

# Tests específicos
pytest tasks/tests/test_auth.py
```

## 📝 Ejemplo de uso

### 1. Registro de usuario
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "jose",
    "email": "jose@example.com",
    "password": "securepass123"
  }'
```

### 2. Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "jose",
    "password": "securepass123"
  }'
```

### 3. Crear tarea (con token)
```bash
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "title": "Completar documentación",
    "description": "Escribir README completo",
    "status": "pending",
    "priority": "high",
    "due_date": "2024-12-31T23:59:59Z"
  }'
```

## 🚀 Deploy

### Railway / Render

1. Conectar repositorio
2. Agregar variables de entorno
3. Deploy automático

### Variables de entorno para producción
```
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DB_NAME=production_db
DB_USER=production_user
DB_PASSWORD=secure_password
DB_HOST=db-host
DB_PORT=5432
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea tu Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push al Branch (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

## 👤 Autor

**Tu Nombre**
- GitHub: (https://github.com/imner/)
- LinkedIn: (https://www.linkedin.com/in/imnermallqui/)

## 🙏 Agradecimientos

- Django REST Framework
- PostgreSQL
- Comunidad de Python

---

⭐️ Si este proyecto te fue útil, considera darle una estrella!
