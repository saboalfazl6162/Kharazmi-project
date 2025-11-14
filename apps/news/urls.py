from django.urls import path
from .views import PostListView,PostCreateView,PostDetailView,PostUpdateView,PostDeleteView,CommentDeleteView

urlpatterns = [
    path('',PostListView.as_view(),name="blog-page"),
    path('posts/create/',PostCreateView.as_view(),name="create-post-page"),
    path('posts/<int:pk>/',PostDetailView.as_view(),name="post-detail-page"),
    path('posts/<int:id>/edit/',PostUpdateView.as_view(),name="update-post-page"),
    path('posts/<int:pk>/delete/',PostDeleteView.as_view(),name="delete-post-page"),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
]