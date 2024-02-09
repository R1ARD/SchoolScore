from django.views.generic import UpdateView, CreateView
from django.db.models import Avg
from .models import Score, Event, SchoolClass
from django.urls import reverse_lazy
from django.shortcuts import  render
from .forms import EventForm
def index(request):
    return render(request, "home.html")

def HighSchoolView(request):
    school_classes = SchoolClass.objects.filter(class_number__gte=5, class_number__lte=11).order_by('class_number', 'class_letter')
    events = Event.objects.all().filter(is_visible=True).order_by('is_below', 'date',)

    # Создаем матрицу для хранения оценок
    score_matrix = []

    for event in events:
        row = {'event': event, 'scores': []}
        for school_class in school_classes:
            score = Score.objects.filter(event=event, schoolclass=school_class).first()
            row['scores'].append(score)
        score_matrix.append(row)

    average_scores = {}

    for school_class in school_classes:
        # Используем агрегацию Avg для вычисления среднего балла по каждому классу
        average_score = Score.objects.filter(schoolclass=school_class).aggregate(Avg('rating'))['rating__avg']

        # Добавляем средний балл в словарь (если не является None)
        average_scores[school_class] = average_score if average_score is not None else 0

    # Создаем словарь для хранения средних баллов среди классов с одинаковыми номерами
    average_scores_by_number = {}

    for school_class in school_classes:
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





    context = {'score_matrix': score_matrix, 'overall_average_scores': overall_average_scores, 'average_scores': average_scores, 'school_classes': school_classes}

    return render(request, 'HighSchool.html', context)


def ElementarySchoolView(request):
    school_classes = SchoolClass.objects.filter(class_number__gte=1, class_number__lte=4).order_by('class_number', 'class_letter')
    events = Event.objects.all().filter(is_visible=True).order_by('is_below', 'date',)

    # Создаем матрицу для хранения оценок
    score_matrix = []

    for event in events:
        row = {'event': event, 'scores': []}
        for school_class in school_classes:
            score = Score.objects.filter(event=event, schoolclass=school_class).first()
            row['scores'].append(score)
        score_matrix.append(row)

    average_scores = {}

    for school_class in school_classes:
        # Используем агрегацию Avg для вычисления среднего балла по каждому классу
        average_score = Score.objects.filter(schoolclass=school_class).aggregate(Avg('rating'))['rating__avg']

        # Добавляем средний балл в словарь (если не является None)
        average_scores[school_class] = average_score if average_score is not None else 0

    # Создаем словарь для хранения средних баллов среди классов с одинаковыми номерами
    average_scores_by_number = {}

    for school_class in school_classes:
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


    context = {'score_matrix': score_matrix, 'overall_average_scores': overall_average_scores, 'average_scores': average_scores, 'school_classes': school_classes}

    return render(request, 'ElementarySchool.html', context)

class ScoreCreateView(CreateView):
    model = Score
    template_name = 'score_create.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('home')

class ScoreUpdateView(UpdateView):
    model = Score
    template_name = 'score_update.html'
    fields = ['rating']

    def get_success_url(self):
        return reverse_lazy('home')

class EventCreateView(CreateView):
    model = Event
    template_name = 'event_create.html'
    form_class = EventForm

    def get_success_url(self):
        return reverse_lazy('home')