from django.urls import path
from .views import QaMainView


urlpatterns = [
    path('',QaMainView.as_view(),name="qa-page")
]