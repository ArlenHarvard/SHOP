from django.db.models import TextChoices

class MyUserRoleEnum(TextChoices):
    USER = 'user', 'Обычный пользователь'
    MANAGER = 'manager', 'Менеджер'
    BOOKKEEPER = 'bookkeeper', 'Бухгалтер'