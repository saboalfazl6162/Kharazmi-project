from django.urls import path
from .views import QaMainView,QuestionCreateView


urlpatterns = [
    path('',QaMainView.as_view(),name="qa-page"),
    path('question/create',QuestionCreateView.as_view(),name="question-create"),
]