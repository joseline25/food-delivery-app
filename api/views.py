
from datetime import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from restaurant.models import Restaurant, OpeningHour
from .serializers import RestaurantSerializer
from rest_framework.decorators import action


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    # get all restaurants

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset
    
    
    # Override the 'create' method
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    # Override the 'retrieve' method
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # Override the 'update' method
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    # Override the 'partial_update' method
    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    # Override the 'destroy' method
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=204)
    
    
    """ 
        To access the overridden CRUD methods in the RestaurantViewSet through the browser, you can use the following URLs:

        List: Retrieve a list of all restaurants.

        URL: GET /restaurants/
        Create: Create a new restaurant.

        URL: POST /restaurants/
        Retrieve: Retrieve details of a specific restaurant.

        URL: GET /restaurants/{pk}/
        Update: Update details of a specific restaurant.

        URL: PUT /restaurants/{pk}/ or PATCH /restaurants/{pk}/
        Partial Update: Update specific fields of a specific restaurant.

        URL: PATCH /restaurants/{pk}/
        Delete: Delete a specific restaurant.

        URL: DELETE /restaurants/{pk}/
    """

    # Custom actions with appropriate methods:

    def action_filter_by_cuisine(self, request, cuisine_slug):
        queryset = self.queryset.filter(cuisines__slug=cuisine_slug)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    

    
    
    @action(detail=True, methods=['get'])
    def is_open(self, request, pk=None):
        restaurant = self.get_object()
        is_open = restaurant.is_open()
        return Response({'is_open': is_open})
    
    @action(detail=True, methods=['get'])
    def average_rating(self, request, pk=None):
        restaurant = self.get_object()
        average_rating = restaurant.average_rating()
        return Response({'average_rating': average_rating})
    
    # @action(detail=True, methods=['get'])
    # def latest_reviews(self, request, pk=None):
    #     restaurant = self.get_object()
    #     latest_reviews = restaurant.latest_reviews()
    #     return Response({'latest_reviews': latest_reviews})

    @action(detail=False, methods=['GET'])
    def action_filter_by_opening_hours(self, request):
        # Assuming you have an 'opening_hours' field in your Restaurant model
        start_time = request.query_params.get('start_time')
        end_time = request.query_params.get('end_time')

        queryset = self.queryset.filter(
            opening_hours__start_time__lte=start_time,
            opening_hours__end_time__gte=end_time
        )
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    """ 
    
    the action_filter_by_opening_hours method is decorated with @action to indicate that
    it's a custom action. It is set to accept GET requests and marked as detail=False 
    since it operates on the entire collection of restaurants.

    The method retrieves the start_time and end_time query parameters from the request 
    using request.query_params.get(). You may need to adjust the actual field names or 
    query parameter names based on your specific implementation.

    Then, it performs a queryset filter based on the provided opening hours using the 
    filter() method.
    
    Modify the filtering conditions based on your Restaurant model structure.

    Finally, the filtered queryset is serialized using the RestaurantSerializer, 
    and the serialized data is returned in a Response.

    Make sure to include the appropriate URL configuration to access this custom action
    in your urls.py file.
    """

    # Override methods as needed (e.g., for filtering, ordering, pagination)
    # Example of overriding 'list' method for custom filtering
    def list(self, request, *args, **kwargs):
        # Perform additional filtering or modification of queryset
        queryset = self.filter_queryset(self.get_queryset())

        # Serialize the queryset
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

   
