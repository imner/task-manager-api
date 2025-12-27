import pytest
from django.utils import timezone
from datetime import timedelta
from tasks.models import Task


@pytest.mark.django_db
class TestTaskModel:
    """
        Tests para el modelo Task
    """
    
    def test_create_task(self, user):
        """
            Test: Crear una tarea básica
        """

        task = Task.objects.create(
            title='Tarea de prueba',
            description='Descripción de prueba',
            owner=user
        )
        
        assert task.id is not None
        assert task.title == 'Tarea de prueba'
        assert task.status == 'pending'
        assert task.priority == 'medium'
        assert task.owner == user
    
    def test_task_str_representation(self, user):
        """
            Test: Representación en string de Task
        """
        
        task = Task.objects.create(
            title='Mi tarea',
            status='in_progress',
            owner=user
        )
        
        assert str(task) == 'Mi tarea - En Progreso'
    
    def test_task_default_values(self, user):
        """
            Test: Valores por defecto de Task
        """
        
        task = Task.objects.create(
            title='Tarea simple',
            owner=user
        )
        
        assert task.status == 'pending'
        assert task.priority == 'medium'
        assert task.description == ''
        assert task.due_date is None
    
    def test_task_is_completed_property(self, user):
        """
            Test: Propiedad is_completed
        """
        
        task = Task.objects.create(
            title='Tarea',
            status='completed',
            owner=user
        )
        
        assert task.is_completed is True
        
        task.status = 'pending'
        assert task.is_completed is False
    
    def test_task_is_pending_property(self, user):
        """
            Test: Propiedad is_pending
        """
        
        task = Task.objects.create(
            title='Tarea',
            status='pending',
            owner=user
        )
        
        assert task.is_pending is True
        
        task.status = 'completed'
        assert task.is_pending is False
    
    def test_task_mark_as_completed(self, user):
        """
            Test: Método mark_as_completed
        """
        
        task = Task.objects.create(
            title='Tarea',
            status='pending',
            owner=user
        )
        
        task.mark_as_completed()
        task.refresh_from_db()
        
        assert task.status == 'completed'
        assert task.is_completed is True
    
    def test_task_mark_as_in_progress(self, user):
        """
            Test: Método mark_as_in_progress
        """
        
        task = Task.objects.create(
            title='Tarea',
            status='pending',
            owner=user
        )
        
        task.mark_as_in_progress()
        task.refresh_from_db()
        
        assert task.status == 'in_progress'
    
    def test_task_is_overdue_no_due_date(self, user):
        """
            Test: Tarea sin fecha de vencimiento no está vencida
        """
        
        task = Task.objects.create(
            title='Tarea',
            owner=user
        )
        
        assert task.is_overdue() is False
    
    def test_task_is_overdue_future_date(self, user):
        """
            Test: Tarea con fecha futura no está vencida
        """
        
        future_date = timezone.now() + timedelta(days=5)
        task = Task.objects.create(
            title='Tarea',
            due_date=future_date,
            owner=user
        )
        
        assert task.is_overdue() is False
    
    def test_task_is_overdue_past_date(self, user):
        """
            Test: Tarea con fecha pasada está vencida
        """

        past_date = timezone.now() - timedelta(days=5)
        task = Task.objects.create(
            title='Tarea',
            due_date=past_date,
            status='pending',
            owner=user
        )
        
        assert task.is_overdue() is True
    
    def test_task_is_overdue_completed_task(self, user):
        """
            Test: Tarea completada no está vencida aunque la fecha haya pasado
        """

        past_date = timezone.now() - timedelta(days=5)
        task = Task.objects.create(
            title='Tarea',
            due_date=past_date,
            status='completed',
            owner=user
        )
        
        assert task.is_overdue() is False
    
    def test_task_ordering(self, user):
        """
            Test: Las tareas se ordenan por created_at descendente
        """
        
        task1 = Task.objects.create(title='Tarea 1', owner=user)
        task2 = Task.objects.create(title='Tarea 2', owner=user)
        task3 = Task.objects.create(title='Tarea 3', owner=user)
        
        tasks = list(Task.objects.all())
        
        assert tasks[0] == task3
        assert tasks[1] == task2
        assert tasks[2] == task1
    
    def test_task_cascade_delete_user(self, user):
        """
            Test: Al eliminar usuario se eliminan sus tareas
        """
        
        Task.objects.create(title='Tarea 1', owner=user)
        Task.objects.create(title='Tarea 2', owner=user)
        
        assert user.tasks.count() == 2

        user.delete()

        assert Task.objects.count() == 0
    
    def test_task_related_name(self, user):
        """
            Test: Related name 'tasks' funciona correctamente
        """
        
        Task.objects.create(title='Tarea 1', owner=user)
        Task.objects.create(title='Tarea 2', owner=user)
        
        assert user.tasks.count() == 2
        assert list(user.tasks.all())