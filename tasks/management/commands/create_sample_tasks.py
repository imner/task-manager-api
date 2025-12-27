from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from tasks.models import Task
import random


class Command(BaseCommand):
    help = 'Crea tareas de ejemplo para testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user',
            type=str,
            help='Username del usuario propietario de las tareas',
        )
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Número de tareas a crear',
        )

    def handle(self, *args, **options):
        username = options.get('user')
        count = options.get('count')
        
        if username:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Usuario "{username}" no encontrado')
                )
                return
        else:
            user = User.objects.first()
            if not user:
                self.stdout.write(
                    self.style.ERROR('No hay usuarios en la base de datos')
                )
                return
        
        statuses = ['pending', 'in_progress', 'completed']
        priorities = ['low', 'medium', 'high']
        
        tasks_created = 0
        
        for i in range(count):
            # Generar fecha aleatoria (algunas vencidas, otras futuras)
            days_offset = random.randint(-10, 30)
            due_date = timezone.now() + timedelta(days=days_offset) if random.choice([True, False]) else None
            
            task = Task.objects.create(
                title=f'Tarea de ejemplo #{i+1}',
                description=f'Esta es la descripción de la tarea #{i+1}. '
                            f'Contiene información detallada sobre lo que hay que hacer.',
                status=random.choice(statuses),
                priority=random.choice(priorities),
                due_date=due_date,
                owner=user
            )
            tasks_created += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'✓ Se crearon {tasks_created} tareas para el usuario "{user.username}"'
            )
        )