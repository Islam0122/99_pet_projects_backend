from django.db import models

class Table(models.Model):
    image = models.ImageField(upload_to='table/%Y/%m', blank=True, null=True)
    number = models.PositiveIntegerField(unique=True)
    capacity = models.PositiveIntegerField()
    location = models.CharField(
        max_length=50,
        choices=[
            ('main', 'Main Hall'),
            ('terrace', 'Terrace'),
            ('vip', 'VIP')
        ]
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Table {self.number} ({self.location}, seats: {self.capacity})"

    class Meta:
        db_table = "tables"
        verbose_name = "Table"
        verbose_name_plural = "Tables"
        ordering = ['number']
