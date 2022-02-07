from django.urls import path
from apps.userauth import views

urlpatterns = [
	path('register/', views.user_register, name="register"),
	path('login/', views.user_login, name="login"),
	path('logout/', views.user_logout, name="logout"),
	path('', views.user_login),
]