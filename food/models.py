from django.db import models

# Create your models here.

# Food Model

class Food(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    number_people = models.IntegerField()
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
