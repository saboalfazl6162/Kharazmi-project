from django import forms
from .models import Question,Answer
from django_summernote.widgets import SummernoteWidget


class QuestionForm(forms.ModelForm):
    """Form definition for Question."""

    class Meta:
        """Meta definition for Questionform."""

        model = Question
        fields = ('title','photo','description')

class AnswerForm(forms.ModelForm):
    """Form definition for Answer."""

    class Meta:
        """Meta definition for Answerform."""

        model = Answer
        fields = ('title','description')
        widgets = {
            'description':SummernoteWidget()
        }