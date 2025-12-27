from django.contrib import admin
from .models import UserProfile, Task
from django.utils.html import format_html
from django.utils import timezone

# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'created_at']
    search_fields = ['user__username', 'user__email', 'location']
    list_filter = ['created_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "owner",
        "status_badge",
        "priority_badge",
        "due_date",
        "is_overdue_badge",
        "created_at"
    ]
    list_filter = ["status", "priority", "created_at", "due_date"]
    search_fields = ["title", "description", "owner__username"]
    readonly_fields = ["created_at", "updated_at", "is_overdue"]
    fieldsets = (
        ('Información básica', {
            'fields': ('title', 'description', 'owner')
        }),
        ('Estado y prioridad', {
            'fields': ('status', 'priority', 'due_date')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def status_badge(self, obj):
        """
            Muestra el estado con colores
        """

        colors = {
            'pending': '#ffc107',
            'in_progress': '#17a2b8',
            'completed': '#28a745',
        }
        color = colors.get(obj.status, "#6c757d")
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = "Estado"

    def priority_badge(self, obj):
        """Muestra la prioridad con colores"""
        colors = {
            'low': '#28a745',
            'medium': '#ffc107',
            'high': '#dc3545',
        }
        color = colors.get(obj.priority, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_priority_display()
        )
    priority_badge.short_description = 'Prioridad'

    def is_overdue_badge(self, obj):
        """
            Muestra si la tarea está vencida
        """

        if obj.is_overdue():
            return format_html(
                '<span style="color: red; font-weight: bold;">⚠️ Vencida</span>'
            )
        return format_html('<span style="color: green;">✓ Al día</span>')
    is_overdue_badge.short_description = 'Vencimiento'
    
    actions = ['mark_as_completed', 'mark_as_in_progress', 'mark_as_pending']
    
    def mark_as_completed(self, request, queryset):
        """
            Acción para marcar tareas como completadas
        """

        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} tarea(s) marcada(s) como completada(s).')
    mark_as_completed.short_description = 'Marcar como completada'
    
    def mark_as_in_progress(self, request, queryset):
        """
            Acción para marcar tareas como en progreso
        """

        updated = queryset.update(status='in_progress')
        self.message_user(request, f'{updated} tarea(s) marcada(s) como en progreso.')
    mark_as_in_progress.short_description = 'Marcar como en progreso'
    
    def mark_as_pending(self, request, queryset):
        """
            Acción para marcar tareas como pendientes
        """
        
        updated = queryset.update(status='pending')
        self.message_user(request, f'{updated} tarea(s) marcada(s) como pendiente(s).')
    mark_as_pending.short_description = 'Marcar como pendiente'