from .api import views
from django.urls import path

urlpatterns = [
    path('login/', views.UserLogin.as_view(), name='login'),
    path('dislike/', views.FestDislike.as_view(), name='dislike')
]
