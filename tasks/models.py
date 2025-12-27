from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# Create your models here.

class UserProfile(models.Model):
    """
        Extiende el modelo User con información adicional del perfil
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"perfil de {self.user.username}"
    
    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuario"

    # Señal para crear automáticamente un perfil cuando se crea un usuario
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **Kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        if hasattr(instance, 'profile'):
            instance.profile.save()


class Task(models.Model):
    """
        Modelo para las tareas del usuario
    """

    STATUS_CHOICES = [
        ("pending", "Pendiente"),
        ("in_progress", "En Progreso"),
        ("completed", "Completada"),
    ]

    PRIORITY_CHOICES = [
        ("low", "Baja"),
        ("medium", "Media"),
        ("high", "Alta"),
    ]

    title = models.CharField(
        max_length=200,
        verbose_name='Título',
        help_text='Título de la tarea'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Descripción',
        help_text='Descripción detallada de la tarea'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Estado',
        help_text='Estado actual de la tarea'
    )
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='medium',
        verbose_name='Prioridad',
        help_text='Nivel de prioridad de la tarea'
    )
    due_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha de vencimiento',
        help_text='Fecha límite para completar la tarea'
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name='Propietario',
        help_text='Usuario que creó la tarea'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Última actualización'
    )

    class Meta:
        verbose_name = "Tarea"
        verbose_name_plural = "Tareas"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["owner", "status"]),
            models.Index(fields=["owner", "priority"]),
            models.Index(fields=["due_date"]),
        ]

    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"
    
    def is_overdue(self):
        """
            Verifica si la tarea está vencida
        """
        
        if self.due_date and self.status != "completed":
            return timezone.now() > self.due_date
        return False
    
    def mark_as_completed(self):
        """
            Marca la tarea como completada
        """

        self.status = "completed"
        self.save(update_fields=["status", "updated_at"])

    def mark_as_in_progress(self):
        """
            Marca la tarea como en progreso
        """

        self.status = "in_progress"
        self.save(update_fields=["status", "updated_at"])

    @property
    def is_completed(self):
        """
            Verifica si la tarea está completada
        """

        return self.status == "completed"
    
    @property
    def is_pending(self):
        """
            Verifica si la tarea está pendiente
        """
    
        return self.status == "pending"
