from django.shortcuts import render
from django.views.generic import TemplateView,CreateView
from .models import Question,Answer
from .forms import AnswerForm,QuestionForm
from django.urls import reverse_lazy

class QaMainView(TemplateView):
    template_name = "qa_page.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = Question.objects.filter(is_active = True)
        return context

class QuestionCreateView(CreateView):
    model = Question
    template_name = "question_create.html"
    form_class = QuestionForm
    success_url = reverse_lazy("qa-page")