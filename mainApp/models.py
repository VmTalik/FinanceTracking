from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Категория расхода', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Категории расходов'
        verbose_name = 'Категория расхода'


class Expense(models.Model):
    description = models.CharField(max_length=150, verbose_name='Описание')
    value = models.PositiveIntegerField(verbose_name='Расход')
    date = models.DateField(verbose_name='Дата')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')

    def __str__(self):
        return f'{self.category_id}__{self.user_id}__{self.date}'

    class Meta:
        verbose_name_plural = 'Расходы'
        verbose_name = 'Расход'
