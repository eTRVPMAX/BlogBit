from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('post/<slug:slug>/', views.post_page, name='post_page'),
    path('tag/<slug:slug>/', views.tagged, name='tagged'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)