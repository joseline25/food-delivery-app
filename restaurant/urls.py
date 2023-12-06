from django.urls import path
from . import views

app_name = "restaurant"

urlpatterns = [
    # login + SignUp
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    
    # Base template
    path('base/', views.base, name='base'),
    path('base_location_restaurant/<int:pk>/',
         views.base_location_restaurant, name='base_location_restaurant'),

    # Restaurant CRUD
    path('', views.restaurant_list, name='restaurant_list'),
    path('restaurant_update/<int:pk>/',
         views.restaurant_update, name="restaurant_update"),
    path('restaurant_delete/<int:pk>/',
         views.restaurant_delete, name="restaurant_delete"),
    
    
    # Food CRUD
    path('food_list/', views.food_list, name='food_list'),
    path('food_update/<int:pk>/',
         views.food_update, name="food_update"),
    path('food_delete/<int:pk>/',
         views.food_delete, name="food_delete"),

]
