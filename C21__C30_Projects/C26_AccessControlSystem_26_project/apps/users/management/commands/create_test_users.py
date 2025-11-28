from django.core.management.base import BaseCommand
from apps.users.models import User, Role, UserRole


class Command(BaseCommand):
    help = 'Создание тестовых пользователей с разными ролями'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Создание тестовых пользователей...'))

        try:
            admin_role = Role.objects.get(name='admin')
            manager_role = Role.objects.get(name='manager')
            user_role = Role.objects.get(name='user')
            guest_role = Role.objects.get(name='guest')
        except Role.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                'Роли не найдены! Сначала выполните: python manage.py loaddata fixtures/initial_data.json'
            ))
            return

        admin_user, created = User.objects.get_or_create(
            email='admin@example.com',
            defaults={
                'first_name': 'Админ',
                'last_name': 'Главный',
                'is_verified': True,
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            UserRole.objects.create(user=admin_user, role=admin_role)
            self.stdout.write(self.style.SUCCESS(f'✓ Создан администратор: admin@example.com / admin123'))
        else:
            self.stdout.write(self.style.WARNING(f'• Администратор уже существует: admin@example.com'))

        manager_user, created = User.objects.get_or_create(
            email='manager@example.com',
            defaults={
                'first_name': 'Менеджер',
                'last_name': 'Опытный',
                'is_verified': True,
            }
        )
        if created:
            manager_user.set_password('manager123')
            manager_user.save()
            UserRole.objects.create(user=manager_user, role=manager_role)
            self.stdout.write(self.style.SUCCESS(f'✓ Создан менеджер: manager@example.com / manager123'))
        else:
            self.stdout.write(self.style.WARNING(f'• Менеджер уже существует: manager@example.com'))

        regular_user, created = User.objects.get_or_create(
            email='user@example.com',
            defaults={
                'first_name': 'Пользователь',
                'last_name': 'Обычный',
                'is_verified': True,
            }
        )
        if created:
            regular_user.set_password('user123')
            regular_user.save()
            UserRole.objects.create(user=regular_user, role=user_role)
            self.stdout.write(self.style.SUCCESS(f'✓ Создан пользователь: user@example.com / user123'))
        else:
            self.stdout.write(self.style.WARNING(f'• Пользователь уже существует: user@example.com'))

        guest_user, created = User.objects.get_or_create(
            email='guest@example.com',
            defaults={
                'first_name': 'Гость',
                'last_name': 'Временный',
                'is_verified': True,
            }
        )
        if created:
            guest_user.set_password('guest123')
            guest_user.save()
            UserRole.objects.create(user=guest_user, role=guest_role)
            self.stdout.write(self.style.SUCCESS(f'✓ Создан гость: guest@example.com / guest123'))
        else:
            self.stdout.write(self.style.WARNING(f'• Гость уже существует: guest@example.com'))

        self.stdout.write(self.style.SUCCESS('\n✅ Готово! Тестовые пользователи созданы.'))
        self.stdout.write(self.style.WARNING('\n📋 Список пользователей:'))
        self.stdout.write('1. admin@example.com / admin123 (Администратор)')
        self.stdout.write('2. manager@example.com / manager123 (Менеджер)')
        self.stdout.write('3. user@example.com / user123 (Пользователь)')
        self.stdout.write('4. guest@example.com / guest123 (Гость)')