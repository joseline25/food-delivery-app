from django.shortcuts import render, get_object_or_404, redirect
from .models import Restaurant, Location, Food
from .forms import RestaurantForm, FoodForm

# location of restaurant for the base

def base(request):
    locations = Location.objects.all()
    return render(request, 'restaurant/base.html', {'locations':locations})


def base_location_restaurant(request, pk):
    # get the specific restaurant
    location = Location.objects.get(pk=pk)
    # get all the restaurants of the location
    restaurants = location.restaurants.all()
    
    context = {'location': location, 'restaurants': restaurants}
    return render(request, 'restaurant/location_restaurants.html', context)


### Login and SignUp

# login
def login(request):
    return render(request, 'restaurant/login.html')

# signup
def signup(request):
    return render(request, 'restaurant/signup.html')


### Restaurant CRUD


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



### Food CRUD

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