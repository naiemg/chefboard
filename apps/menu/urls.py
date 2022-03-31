from django.urls import path
from apps.menu import views

urlpatterns = [
	path('dashboard/', views.dashboard, name="dashboard"),
	path('category/<int:rest_id>/', views.read_category, name="read_category"),
	path('restaurant/create/', views.create_restaurant, name="create_restaurant"),
	path('restaurant/<int:rest_id>/edit/', views.edit_restaurant, name="edit_restaurant"),

]