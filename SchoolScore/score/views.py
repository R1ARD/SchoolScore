from django.views.generic import ListView, UpdateView, CreateView
from django.db.models import Avg
from .models import Score, Event, SchoolClass
from django.urls import reverse_lazy

class ScoreListView(ListView):
    model = Score
    template_name = 'dashboard.html'
    context_object_name = 'score_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event_list'] = Event.objects.all()
        context['schoolClass_list'] = SchoolClass.objects.all()
        context['table_data'] = self.get_table_data()
        context['average_scores'] = self.get_average_scores()
        return context

    def get_table_data(self):
        table_data = []
        events = Event.objects.all()
        school_classes = SchoolClass.objects.all()

        for event in events:
            row = {'event': event, 'scores': []}
            for school_class in school_classes:
                score = Score.objects.filter(event=event, schoolclass=school_class).first()
                row['scores'].append(score)
            table_data.append(row)
        return table_data

    def get_average_scores(self):
        average_scores = []
        school_classes = SchoolClass.objects.all()

        avg_row = {'name': 'Средний по классу', 'avgs': []}
        for school_class in school_classes:
            avg_score = Score.objects.filter(schoolclass=school_class).aggregate(Avg('rating'))['rating__avg']
            avg_row['avgs'].append(avg_score)
        average_scores.append(avg_row)

        return average_scores

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