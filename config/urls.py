from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('dashboard-website-1372/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('news/', include('apps.news.urls')),
    path('users/', include('apps.users.urls')),
    path('question-answer/', include('apps.qa.urls')),
    path('summernote/', include('django_summernote.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
