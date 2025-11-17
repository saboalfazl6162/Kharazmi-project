from django.urls import path 
from .views import SignUpView,LoginView,LogoutView,ProfileView,UserDetailView,SelectMainPointView


urlpatterns = [
    path('signup/select-axis/',SelectMainPointView.as_view(),name="select-mainpoint"),
    path("signup/",SignUpView.as_view(),name="signup"),
    path("login/",LoginView.as_view(),name="login"),
    path("logout/",LogoutView.as_view(),name="logout"),
    path("<str:username>",UserDetailView.as_view(),name="user-profile"),
    path('',ProfileView.as_view(),name="my-profile"),
]