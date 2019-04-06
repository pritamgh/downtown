from django.urls import path

from .api import views

urlpatterns = [
    path('auth/login/', views.OrganizationLogin.as_view(), name="login"),
    path('list/', views.OrganizationList.as_view(), name="list"),
    path('create/', views.OrganizationCreate.as_view(), name="create"),
    path('update/', views.OrganizationUpdate.as_view(), name="update"),
    path('dashboard/', views.OrganizationDashboard.as_view(), name="dashboard")
]
