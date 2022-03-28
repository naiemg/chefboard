from django.urls import path
from apps.userauth import views

urlpatterns = [
	path('dashboard/', views.dashboard, name="dashboard"),
]