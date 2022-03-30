from django.urls import path
from .views import RestaurantAPIView, CategoryAPIView, MenuItemAPIView

urlpatterns = [
    path('restaurant/', RestaurantAPIView.as_view()),
    path('restaurant/<int:id>/', RestaurantAPIView.as_view()),
    
    path('category/', CategoryAPIView.as_view()),
    path('category/<int:id>/', CategoryAPIView.as_view()),
    
    path('menu_item/', MenuItemAPIView.as_view()),
    path('menu_item/<int:id>/', MenuItemAPIView.as_view()),
]