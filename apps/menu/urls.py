from django.urls import path
from apps.menu import views

urlpatterns = [
	path('dashboard/', views.dashboard, name="dashboard"),
]