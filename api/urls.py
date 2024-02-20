from django.urls import path, include
from rest_framework import routers
from .views import RestaurantViewSet

router = routers.DefaultRouter()
router.register(r'restaurants', RestaurantViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('restaurants/filter-by-opening-hours/', RestaurantViewSet.as_view({'get': 'action_filter_by_opening_hours'}), name='filter-by-opening-hours'),
    path('restaurants/<int:pk>/is_open/', RestaurantViewSet.as_view({'get': 'is_open'}), name='is_open'),
    path('restaurants/<int:pk>/average-rating/', RestaurantViewSet.as_view({'get': 'average_rating'}), name='restaurant-average-rating'),
    # path('restaurants/<int:pk>/latest-reviews/', RestaurantViewSet.as_view({'get': 'latest_reviews'}), name='restaurant-latest-reviews'),
    

]
