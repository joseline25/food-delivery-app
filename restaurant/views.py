from django.shortcuts import render, get_object_or_404, redirect
from .models import Restaurant, Location, Food, OpeningHour
from .forms import RestaurantForm, FoodForm, OpeningHourForm
from django.db.models import Q
# search with django-watson
from watson import search as watson
from watson import search as watson_search
from functools import reduce
import operator

# Pagination
from django.core.paginator import Paginator

# to test if the restaurant is actually open
from .helpers import is_restaurant_open



# location of restaurant for the base


def base(request):
    locations = Location.objects.all()
    return render(request, 'restaurant/base.html', {'locations': locations})


def base_location_restaurant(request, pk):
    # get the specific restaurant
    location = Location.objects.get(pk=pk)
    # get all the restaurants of the location
    restaurants = location.restaurants.all()

    context = {'location': location, 'restaurants': restaurants}
    return render(request, 'restaurant/location_restaurants.html', context)


# Login and SignUp

# login
def login(request):
    return render(request, 'restaurant/login.html')

# signup


def signup(request):
    return render(request, 'restaurant/signup.html')


def search_restaurants(request):
    location = request.GET.get('location')
    restaurant = request.GET.get('restaurant')

    q_objects = Q()

    if location:
        q_objects &= Q(location__name__icontains=location)

    if restaurant:
        search_fields = ['name', 'cuisines__name',
                         'menus__name', 'category__name']
        # q_objects &= Q(name__icontains=restaurant) | Q(cuisines__name__icontains=restaurant) | Q(category__name__icontains=restaurant)
        queries = [Q(**{field + '__icontains': restaurant})
                   for field in search_fields]
        # q_objects.append(reduce(operator.or_, queries))
        for query in queries:
            q_objects |= query

    restaurants = Restaurant.objects.filter(q_objects)
    search_query_str = str(q_objects)  # Convert Q object to string query

   # Use Watson's search function to perform the search
    search_results = watson_search.search(
        search_query_str, models=(Restaurant,))

    # restaurants = watson.filter(Restaurant, q_objects)
    # Perform the search query based on your requirements
    # restaurants = Restaurant.objects.filter(
    #     location__name__icontains=location,
    #     name__icontains=restaurant,
    #     # add more filters as needed
    # )
    
    
    # Pagination
    
    # set to 10 restaurants per pages
    paginator = Paginator(restaurants, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'restaurants': restaurants,
        # print search_results and compare to restaurants
        'search_results': search_results,
        'location': location,
        'restaurant': restaurant,
        'page_obj':page_obj,
    }
    return render(request, 'restaurant/search_results.html', context)


"""  



def search_restaurants(request):
    location = request.GET.get('location')
    search_query = request.GET.get('search_query')
    cuisines = request.GET.getlist('cuisines')  # Assuming cuisines are selected as checkboxes
    menus = request.GET.getlist('menus')  # Assuming menus are selected as checkboxes

    q_objects = Q()

    if location:
        q_objects &= Q(location__name__icontains=location)

    if search_query:
        q_objects &= Q(name__icontains=search_query) | Q(cuisines__name__icontains=search_query) | Q(menus__name__icontains=search_query)

    if cuisines:
        q_objects &= Q(cuisines__name__in=cuisines)

    if menus:
        q_objects &= Q(menus__name__in=menus)

    restaurants = Restaurant.objects.filter(q_objects)

    context = {
        'restaurants': restaurants,
        'location': location,
        'search_query': search_query,
        'cuisines': cuisines,
        'menus': menus,
    }
    return render(request, 'search_results.html', context)
"""


def search_restaurants_watson(request):
    search_query = request.GET.get('search_query')

    if search_query:
        restaurants = watson.filter(Restaurant, search_query)
    else:
        restaurants = Restaurant.objects.all()

    context = {
        'restaurants': restaurants,
        'search_query': search_query,
    }
    return render(request, 'search_results.html', context)


# Restaurant CRUD


# list of restaurants
def restaurant_list(request):
    context = {}
    # get all the restaurants
    restaurants = Restaurant.objects.all()
    context['restaurants'] = restaurants
    # get the form
    form = RestaurantForm()
    context['form'] = form
    # create a new restaurant
    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('restaurant:restaurant_list')
        else:
            print(form.errors)

    return render(request, 'restaurant/restaurant_list.html', context)


# get the details of a restaurant
def restaurant_details(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    form = OpeningHourForm()
    if request.method == 'POST':
        form = OpeningHourForm(request.POST)
        if form.is_valid():
            # make sure that I do not have the same weekday set up many times

            # get the weekday of the form
            weekday = int(form.cleaned_data['weekday'])
            # get all the entry for that weekday for the specific restaurant
            existing_opening_hours = OpeningHour.objects.filter(
                restaurant=restaurant, weekday=weekday)
            # Check if existing opening hours exist for the specified weekday and restaurant combination
            if existing_opening_hours:
                # Delete existing opening hours
                existing_opening_hours.delete()

            # now save the form
            opening_hours = form.save(commit=False)
            opening_hours.restaurant = restaurant
            opening_hours.save()
            return redirect('restaurant:restaurant_details', pk=pk)
    else:
        print(form.errors)
        form = OpeningHourForm()

    # get the opening hours of the restaurant
    opening_hours = OpeningHour.objects.filter(restaurant=restaurant)
    context = {'restaurant': restaurant,
               'form': form, 'opening_hours': opening_hours}
    return render(request, 'restaurant/restaurant_details.html', context)

# update an existing restaurant


def restaurant_update(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if request.method == 'POST':
        form = RestaurantForm(request.POST, instance=restaurant)
        if form.is_valid():
            form.save()
            return redirect('restaurant:restaurant_list')
    else:
        form = RestaurantForm(instance=restaurant)
    return render(request, 'restaurant/restaurant_list.html', {'form': form})


# delete an existing restaurant
def restaurant_delete(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if request.method == 'POST':
        restaurant.delete()
        return redirect('restaurant_list')
    return render(request, 'restaurant/restaurant_delete.html', {'restaurant': restaurant})


# Food CRUD

def food_list(request):
    foods = Food.objects.all()
    form = FoodForm()
    context = {'foods': foods, 'form': form}
    if request.method == 'POST':
        form = FoodForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('restaurant:food_list')
    else:
        print(form.errors)

    return render(request, 'restaurant/food_list.html', context)


def food_update(request, pk):
    food = get_object_or_404(Food, pk=pk)
    if request.method == 'POST':
        form = FoodForm(request.POST, instance=food)
        if form.is_valid():
            form.save()
            return redirect('restaurant:food_list')
    else:
        form = FoodForm(instance=food)
    return render(request, 'restaurant/food_list.html', {'form': form})


def food_delete(request, pk):
    food = get_object_or_404(Food, pk=pk)
    if request.method == 'POST':
        food.delete()
        return redirect('food_list')
    return render(request, 'food_delete.html', {'food': food})
