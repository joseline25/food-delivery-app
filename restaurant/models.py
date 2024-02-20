from django.db import models
from watson import search as watson
from datetime import datetime
from django.apps import apps
from django.contrib.auth.models import User
from food.models import Food

# Create your models here.


# Restaurant Model

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    location = models.ForeignKey(
        'Location', on_delete=models.CASCADE, related_name='restaurants')
    cuisines = models.ManyToManyField('Cuisine', related_name='restaurants')
    category = models.ManyToManyField(
        "MenuCategory", related_name='restaurants')
    menus = models.ManyToManyField('Menu', related_name='menu_restaurants')

    search_fields = ['name', 'location', 'cuisines', 'menus', 'category']

    def __str__(self):
        return f"{self.name}"

    # if the restaurant is actually open or not

    def is_open(self):
        now = datetime.now().time()
        current_weekday = datetime.now().weekday()

        opening_hours = self.opening_hours.filter(
            weekday=current_weekday).first()

        if opening_hours :
            if opening_hours.open_time and opening_hours.open_time <= now <= opening_hours.close_time:
                return True

        return False
    
    def average_rating(self):
        # Calculate and return the average rating for the restaurant
        ratings = self.rating
        if ratings:
            
            return round(ratings, 2)
        return None
    
    """ When having ratings from users 
    
        def get_average_rating(self):
            # Calculate and return the average rating for the restaurant
        ratings = self.reviews.values_list('rating', flat=True)
        if ratings:
            average_rating = sum(ratings) / len(ratings)
            return round(average_rating, 2)
        return None
    """

    # def latest_reviews(self, num_reviews=5):
    #     # Retrieve the latest reviews for the restaurant
    #     return self.reviews.order_by('-created_at')[:num_reviews]


# to perform advanced search of restaurant using django-watson
watson.register(Restaurant)


# OpeningHour Model

class OpeningHour(models.Model):
    WEEKDAY_CHOICES = [
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
        (7, 'Sunday'),
    ]

    restaurant = models.ForeignKey(
        Restaurant, related_name='opening_hours', on_delete=models.CASCADE)  # not here
    weekday = models.IntegerField(choices=WEEKDAY_CHOICES)
    open_time = models.TimeField(null=True, blank=True)
    close_time = models.TimeField(null=True, blank=True)

    # r.opening_hours.all()

    def __str__(self):
        return f"{self.restaurant} - {self.get_weekday_display()}"

# Cuisine Model


class Cuisine(models.Model):
    name = models.CharField(max_length=255)
    origin = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


# Location Model

class Location(models.Model):
    name = models.CharField(max_length=255)
    lattide = models.CharField(max_length=255, blank=True, null=True)
    longitude = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"




class RestaurantFood():
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    price = models.DecimalField()





# Menu Model

class Menu(models.Model):
    name = models.CharField(max_length=255)

    foods = models.ManyToManyField(Food, related_name='menus')
    categories = models.ManyToManyField('MenuCategory', related_name='menus')

    def __str__(self):
        return f"{self.name}"


# Menu Category Model:
""" This model represents the categories of food items that restaurants offer."""


class MenuCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.name}"







class Admin(User):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='admin_profile')
    address = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self):
        return f"{self.user.username}"
    
    
class RestaurantOwner(User):
    restaurants = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='owner')
    
    def __str__(self):
        return f"{self.username}"

# Client Model
class Client(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='client_profile')
    address = models.CharField(max_length=255, blank=True, null=True)
    orders = models.ManyToManyField('Order', related_name='client_orders')

    def __str__(self):
        return f"{self.user.username}"
    
    
# define the user type 
class UserType(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type_choices = [
        ('admin', 'Admin'),
        ('owner', 'Restaurant Owner'),
        ('user', 'User')
    ]
    user_type = models.CharField(max_length=10, choices=type_choices)




# Order Model

class Order(models.Model):
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name='orders_client')
    restaurant = models.ManyToManyField(
        Restaurant, through='RestaurantOrder')
    food_items = models.ManyToManyField(Food, related_name='orders')
    order_total = models.DecimalField(max_digits=6, decimal_places=2)
    delivery_address = models.CharField(
        max_length=255, blank=True, null=True)
    is_delivered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_default_delivery_address(self):
        return self.client.address

    def __str__(self):
        return f"{self.client.username}  {self.restaurant.name}"


class RestaurantOrder(models.Model):
    order = models.ForeignKey(
        'Order', related_name='restaurant_order', on_delete=models.CASCADE)
    restaurant = models.ForeignKey(
        'Restaurant', related_name='restaurant_order', on_delete=models.CASCADE)


# Article Model:
""" This model represents articles written by restaurant owners """


class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name='articles')

    def __str__(self):
        return f"{self.title}"


# Payment Model:
""" This model represents the payment details for an order """


class Payment(models.Model):
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name='payments')
    payment_method = models.CharField(max_length=255)
    total_amount = models.DecimalField(max_digits=6, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.payment_method}"


# Rating Model:
""" This model represents the ratings and reviews given by users to restaurants. """


class Rating(models.Model):
    user = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name='ratings')
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name='ratings')
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rating}"
