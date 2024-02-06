from django.utils import timezone
from score.models import Event, SchoolClass, Score

# Предполагается, что у вас уже есть созданные экземпляры Event и SchoolClass
events = Event.objects.all()
school_classes = SchoolClass.objects.all()

# Проходим по всем комбинациям
for event in events:
    for school_class in school_classes:
        # Создаем объект Score для каждой комбинации
        score = Score.objects.create(
            schoolclass=school_class,
            event=event,
            rating=None  # Можете установить значение по умолчанию или оставить как None
        )

        # Опционально: Выводим созданный объект Score для проверки
        print(f"Создан объект Score: {score}")
