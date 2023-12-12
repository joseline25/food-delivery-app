from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Food)
admin.site.register(Ingredient)
admin.site.register(Category)
admin.site.register(FoodIgredient)
# admin.site.register(Category)