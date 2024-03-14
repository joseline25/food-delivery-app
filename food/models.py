from django.db import models

# Create your models here.

# Food Model

class Food(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    number_people = models.IntegerField(blank=True, null=True)
    ingredients = models.ManyToManyField(
        'Ingredient',  through='FoodIgredient')
    categories = models.ManyToManyField(
        'Category', related_name='category_foods')

    def __str__(self):
        if self.number_people:
            return f"{self.name} for {self.number_people}"
        else:
            return f"{self.name}"


class FoodIgredient(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=7, decimal_places=3)
    
    def __str__(self):
        return f"{self.ingredient.name} in {self.food.name}"

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
    
    
class Pack(models.Model):
    name= models.CharField(max_length=255)
    number_of_people = models.IntegerField()
    foods=models.ManyToManyField(Food, related_name='packs')
    categories = models.ManyToManyField(Category, related_name='packs_cat')
    
    def __str__(self):
        return f"{self.name} for {self.number_of_people}"
