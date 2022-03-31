from django.urls import path
from apps.menu import views

urlpatterns = [
	path('dashboard/', views.dashboard, name="dashboard"),
	
	path('restaurant/create/', views.restaurant_create, name="restaurant_create"),
	path('restaurant/<int:rest_id>/category/', views.restaurant_read_categories, name="restaurant_read_categories"),
	path('restaurant/<int:rest_id>/update/', views.restaurant_update, name="restaurant_update"),
]