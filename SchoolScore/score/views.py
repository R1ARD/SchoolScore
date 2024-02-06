from django.views.generic import ListView, UpdateView, CreateView
from django.db.models import Avg
from .models import Score, Event, SchoolClass
from django.urls import reverse_lazy
from django.shortcuts import redirect, render

class ScoreListView(ListView):
    model = Score
    template_name = 'HighSchool.html'
    context_object_name = 'score_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event_list'] = Event.objects.all()
        context['schoolClass_list'] = SchoolClass.objects.all()


def score_table(request):
    classes = SchoolClass.objects.all()
    events = Event.objects.all()

    # Создаем матрицу для хранения оценок
    score_matrix = [[None] * (len(classes) + 1) for _ in range(len(events) + 1)]

    # Заполняем первую строку названиями классов
    for j, school_class in enumerate(classes):
        score_matrix[0][j + 1] = school_class

    # Заполняем первый столбец названиями мероприятий
    for i, event in enumerate(events):
        score_matrix[i + 1][0] = event

    # Заполняем оценки в соответствующих ячейках
    for i, event in enumerate(events):
        for j, school_class in enumerate(classes):
            try:
                score = Score.objects.get(schoolclass=school_class, event=event)
                score_matrix[i + 1][j + 1] = score
            except Score.DoesNotExist:
                score_matrix[i + 1][j + 1] = None

    average_scores = {}

    for school_class in classes:
        # Используем агрегацию Avg для вычисления среднего балла по каждому классу
        average_score = Score.objects.filter(schoolclass=school_class).aggregate(Avg('rating'))['rating__avg']

        # Добавляем средний балл в словарь (если не является None)
        average_scores[school_class] = average_score if average_score is not None else 0

    # Создаем словарь для хранения средних баллов среди классов с одинаковыми номерами
    average_scores_by_number = {}

    for school_class in classes:
        class_number = school_class.class_number

        # Если номер класса уже есть в словаре, добавляем текущий средний балл
        if class_number in average_scores_by_number:
            average_scores_by_number[class_number].append(average_scores[school_class])
        else:
            # Если номер класса отсутствует в словаре, создаем новую запись
            average_scores_by_number[class_number] = [average_scores[school_class]]

    # Вычисляем средний балл из средних баллов для каждого номера класса
    overall_average_scores = {}

    for class_number, scores_list in average_scores_by_number.items():
        # Исключаем None из списка перед вычислением среднего балла
        valid_scores_list = [score for score in scores_list if score is not None]

        # Вычисляем средний балл (если есть допустимые значения)
        overall_average_scores[class_number] = {'avg_score': sum(valid_scores_list) / len(valid_scores_list) if valid_scores_list else 0,
                                                'class_count': len(scores_list)}

    context = {'score_matrix': score_matrix, 'overall_average_scores': overall_average_scores, 'average_scores': average_scores}
    return render(request, 'HighSchool.html', context)


def create_all_score_combinations(request):
    # Получите все существующие экземпляры SchoolClass и Event
    school_classes = SchoolClass.objects.all()
    events = Event.objects.all()

    # Создайте экземпляры Score для всех комбинаций
    for school_class in school_classes:
        for event in events:
            Score.objects.create(schoolclass=school_class, event=event)

    # Перенаправьте на страницу успеха или домашнюю страницу
    return redirect('')  # Измените 'success_page' на фактическое имя страницы успеха или URL


class ScoreCreateView(CreateView):
    model = Score
    template_name = 'score_create.html'  # Замените на ваш шаблон
    fields = '__all__'  # Укажите необходимые поля для создания


    def get_success_url(self):
        return reverse_lazy('dashboard')  # Замените 'dashboard' на имя вашего URL-шаблона

class ScoreUpdateView(UpdateView):
    model = Score
    template_name = 'score_update.html'  # Замените на ваш шаблон
    fields = ['rating']  # Укажите необходимые поля для изменения

    def get_success_url(self):
        return reverse_lazy('dashboard')