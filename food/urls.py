from django.urls import path
from . import views

app_name = "food"

urlpatterns = [
    
    # Food
    path('foods/', views.FoodListView.as_view(), name='food_list'),
    path('foods/<int:pk>/', views.FoodDetailView.as_view(), name='food-detail'),
    path('foods/create/', views.FoodCreateView.as_view(), name='food-create'),
    path('foods/<int:pk>/update/', views.FoodUpdateView.as_view(), name='food-update'),
    path('foods/<int:pk>/delete/', views.FoodDeleteView.as_view(), name='food-delete'),
    
    # Pack
    path('', views.PackView.as_view(), name='pack'),
]
