from rest_framework import serializers
from restaurant.models import *
from food.models import *

#GET Serializers 


# Location 
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


# Cuisine
class CuisineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuisine
        fields = '__all__'


# Ingredient 
class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


# Category 
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


# Food 
class FoodSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)
    categories = CategorySerializer(many=True)

    class Meta:
        model = Food
        fields = '__all__'


# FoodIgredient 
class FoodIgredientSerializer(serializers.ModelSerializer):
    food = FoodSerializer()
    ingredient = IngredientSerializer()
    class Meta:
        model = FoodIgredient
        fields = '__all__'


# Menu 
class MenuSerializer(serializers.ModelSerializer):
    foods = FoodSerializer(many=True)
    categories = CategorySerializer(many=True)
    class Meta:
        model = Menu
        fields = '__all__'
        



# MenuCategory 
class MenuCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuCategory
        fields = '__all__'


# Restaurant 
class RestaurantSerializer(serializers.ModelSerializer):
    
    menus = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)
    cuisines = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)
    category = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)
    is_open = serializers.SerializerMethodField()  # for the method is_open of Restaurant

   

    class Meta:
        model = Restaurant
        fields = [
            # All fields 
            'id',
            'name',
            'description',
            'rating',
            'location',
            'menus',
            'cuisines',
            'category',
            'is_open',  # include the added field
            'average_rating',
            # 'latest_reviews',
        ]

    def get_is_open(self, instance):
        return instance.is_open()  # call the is_open method
    
    def get_average_rating(self, instance):
        return instance.average_rating()
    
    # def get_latest_reviews(self, instance):
    #     return instance.latest_reviews()


# POST Serializers

# Restaurant
class RestaurantSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'
        
        
# Food 
class FoodSerializerPost(serializers.ModelSerializer):
    
    class Meta:
        model = Food
        fields = '__all__'

# Menu 
class MenuSerializerPost(serializers.ModelSerializer):
   
    class Meta:
        model = Menu
        fields = '__all__'
        