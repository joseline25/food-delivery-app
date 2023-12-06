from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User

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

    def __str__(self):
        return f"{self.name}"


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


# Food Model

class Food(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    ingredients = models.ManyToManyField(
        'Ingredient',  through='FoodIgredient')
    categories = models.ManyToManyField(
        'Category', related_name='category_foods')

    def __str__(self):
        return f"{self.name}"


class FoodIgredient(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=7, decimal_places=3)


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


# Ingredient Model

class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    season = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


# Category Model of a food

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


# Client Model


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True, null=True)
    orders = models.ManyToManyField('Order', related_name='client_orders')

    def __str__(self):
        return f"{self.user.username}"


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