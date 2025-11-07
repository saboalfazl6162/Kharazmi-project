from django.urls import path
from .views import HomePageView,GlobalSearchView,AboutPageView,ContactPageView


urlpatterns = [
    path('',HomePageView.as_view(),name="home-page"),
    path('contact-us/',ContactPageView.as_view(),name="about-page"),
    path('about-us/',AboutPageView.as_view(),name="about-page"),
    path('search/', GlobalSearchView.as_view(), name='global-search'),
]