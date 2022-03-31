from django.urls import path
from apps.userauth import views

urlpatterns = [
	path('register/', views.user_register, name="register"),
	path('login/', views.user_login, name="login"),
	path('logout/', views.user_logout, name="logout"),
	path('', views.user_login),
	path('profile/', views.profile, name="profile"),
	
	path('config/', views.stripe_config),
	path('create-checkout-session/', views.create_checkout_session),
	path('success/', views.success),
    path('cancel/', views.cancel),
    path('webhook/', views.stripe_webhook),
]