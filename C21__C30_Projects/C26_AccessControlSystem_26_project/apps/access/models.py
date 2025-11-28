from django.db import models


class BusinessElement(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название элемента")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Бизнес-элемент"
        verbose_name_plural = "Бизнес-элементы"
        ordering = ['name']

    def __str__(self):
        return self.name


class AccessRolesRules(models.Model):
    role = models.ForeignKey(
        'users.Role',
        on_delete=models.CASCADE,
        related_name='access_rules',
        verbose_name="Роль"
    )
    element = models.ForeignKey(
        BusinessElement,
        on_delete=models.CASCADE,
        related_name='access_rules',
        verbose_name="Бизнес-элемент"
    )
    read_permission = models.BooleanField(default=False, verbose_name="Чтение своих объектов")
    read_all_permission = models.BooleanField(default=False, verbose_name="Чтение всех объектов")
    create_permission = models.BooleanField(default=False, verbose_name="Создание")
    update_permission = models.BooleanField(default=False, verbose_name="Обновление своих объектов")
    update_all_permission = models.BooleanField(default=False, verbose_name="Обновление всех объектов")
    delete_permission = models.BooleanField(default=False, verbose_name="Удаление своих объектов")
    delete_all_permission = models.BooleanField(default=False, verbose_name="Удаление всех объектов")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Правило доступа"
        verbose_name_plural = "Правила доступа"
        unique_together = ('role', 'element')
        ordering = ['role__name', 'element__name']

    def __str__(self):
        return f"{self.role.name} -> {self.element.name}"

    def get_permissions_summary(self):
        perms = []
        if self.read_all_permission:
            perms.append("Читать все")
        elif self.read_permission:
            perms.append("Читать свои")

        if self.create_permission:
            perms.append("Создавать")

        if self.update_all_permission:
            perms.append("Редактировать все")
        elif self.update_permission:
            perms.append("Редактировать свои")

        if self.delete_all_permission:
            perms.append("Удалять все")
        elif self.delete_permission:
            perms.append("Удалять свои")

        return ", ".join(perms) if perms else "Нет прав"
