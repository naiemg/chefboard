from django.urls import path
from apps.display import views

urlpatterns = [	
	path('screen/design/<int:rest_id>/', views.design_screen, name="screen_design"),
]