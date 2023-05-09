from django.contrib import admin
from django.urls import path
from SearchEngine import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('videos/', views.trending, name='trending'),
    path('search/', views.search, name='search'),
    path('saved/<str:email_id>/', views.saved, name='saved'),
    path('liked/<str:email_id>/<str:video_id>', views.liked, name='liked'),
]
