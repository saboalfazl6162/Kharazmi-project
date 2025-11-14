from django import forms
from django_summernote.widgets import SummernoteWidget

from django import forms
from .models import Post
from django_summernote.widgets import SummernoteWidget

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "thumbnail",
            "short_description",
            "article_course",
            "description",
            "meta_name",
            "meta_description",
            "meta_keywords",
        ]
        widgets = {
            "description": SummernoteWidget(attrs={"placeholder": "توضیحات"}),
            "title": forms.TextInput(attrs={"placeholder": "موضوع"}),
            "short_description": forms.TextInput(attrs={"placeholder": "توضیحات کوتاه"}),
            "meta_name": forms.TextInput(attrs={"placeholder": "نام متا"}),
            "meta_description": forms.TextInput(attrs={"placeholder": "توضیح متا"}),
            "meta_keywords": forms.TextInput(attrs={"placeholder": "کلمات کلیدی"}),
        }
