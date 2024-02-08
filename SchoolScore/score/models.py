# models.py
from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.db.models import Max


class SchoolClass(models.Model):
    class_number = models.IntegerField(
        validators=[
            MinValueValidator(1, message='Номер класса должен быть не менее 1.'),
            MaxValueValidator(11, message='Номер класса должен быть не более 11.')
        ],
        verbose_name='Номер класса'
    )
    class_letter = models.CharField(
        max_length=1,
        validators=[
            RegexValidator(
                regex='^[А-Я]$',
                message='Введите одну кириллическую букву.',
                code='invalid_class_letter'
            )
        ],
        verbose_name='Буква класса'
    )

    def __str__(self):
        return f"{self.class_number}{self.class_letter}"


class Event(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название мероприятия')
    date = models.DateField(verbose_name='Дата мероприятия', blank=True, null=True)
    is_visible = models.BooleanField(default=True, verbose_name='Видимость')
    is_below = models.BooleanField(default=False, verbose_name='Прикрепить снизу')
    def __str__(self):
        return f"{self.name} - {self.date}"

class Score(models.Model):
    schoolclass = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, verbose_name='Класс')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='Мероприятие')
    create_date = models.DateTimeField(verbose_name='Дата оценки', auto_now_add=True, null=True)
    rating = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, message='Оценка должна быть не менее 1.'),
            MaxValueValidator(5, message='Оценка должна быть не более 5.')
        ],
        blank=True, null=True,
        verbose_name='Оценка'
    )
    def __str__(self):
        return f"{self.rating}"