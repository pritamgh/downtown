from django.urls import path
from .api import views


urlpatterns = [

    path('home/', views.HomePage.as_view(), name="home"),
    path('create/', views.FestCreate.as_view(), name="create"),
    path('update/', views.FestUpdate.as_view(), name="update"),
    path('delete/', views.FestDelete.as_view(), name="delete"),
    path('details/', views.FestDetails.as_view(), name="details"),
    path('liked/', views.FestLiked.as_view(), name="liked")
]
