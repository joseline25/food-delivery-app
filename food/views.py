from .forms import PackForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.shortcuts import render

# Create your views here.

""" 
CRUD Operations: You can perform Create, Read, Update, and Delete operations for each
model (Food, Ingredient, Category, Pack). This allows you to manage the data stored in
the database.

Relationships:

Food-Ingredient Relationship: The Food model has a ManyToMany relationship with the 
Ingredient model through the FoodIngredient model. This allows you to associate multiple
ingredients with a food item and specify the quantity.
Food-Category Relationship: The Food model has a ManyToMany relationship with the Category
model. This allows you to categorize food items into multiple categories.
Pack Model: The Pack model represents a pack of food items for a specific number of people.

Querying and Filtering: You can write queries to retrieve specific data from the database. 
For example, you can fetch all foods belonging to a particular category, all ingredients 
associated with a food, or packs suitable for a specific number of people.

Validation: You can implement validation logic to ensure that certain fields have valid 
values. For example, you can enforce that the price field is always greater than zero, or
that the number_of_people field in the Pack model is always a positive integer.

Displaying Data: You can customize the string representation (__str__ method) for each 
model to display meaningful information when objects are printed or displayed in the 
Django admin interface.

Admin Interface: Django provides an admin interface that allows you to manage your models
and data easily. You can register your models in the admin.py file and customize the admin
interface to suit your needs.
"""

# Food

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Food, Pack


class FoodListView(ListView):
    model = Food
    template_name = 'food/food_list.html'
    # The variable name to be used in the template for the food list
    context_object_name = 'foods'


class FoodDetailView(DetailView):
    model = Food
    template_name = 'food/food_detail.html'
    # The variable name to be used in the template for the food object
    context_object_name = 'food'


class FoodCreateView(CreateView):
    model = Food
    template_name = 'food/food_create.html'
    fields = ['name', 'description', 'price',
              'number_people', 'ingredients', 'categories']


class FoodUpdateView(UpdateView):
    model = Food
    template_name = 'food_update.html'  # Replace with your desired template name
    fields = ['name', 'description', 'price',
              'number_people', 'ingredients', 'categories']


class FoodDeleteView(DeleteView):
    model = Food
    # Replace with your desired template name
    template_name = 'food_confirm_delete.html'
    # The URL to redirect to after successful deletion
    success_url = reverse_lazy('food-list')


# Pack


class PackView(View):
    template_name = 'food/pack.html'  

    # get all packs available
    def get(self, request):
        packs = Pack.objects.all()
        return render(request, self.template_name, {'packs': packs})

    # create a pack
    def post(self, request):
        form = PackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('food:pack')
        return render(request, self.template_name, {'form': form})

    # get the details of a pack
    def get_object(self, pk):
        return get_object_or_404(Pack, pk=pk)

    def get_context_data(self, pk=None):
        context = {}
        if pk:
            pack = self.get_object(pk)
            context['pack'] = pack
        context['form'] = PackForm()
        return context

    def get(self, request, pk=None):
        context = self.get_context_data(pk)
        return render(request, self.template_name, context)

    def post(self, request, pk=None):
        if pk:
            pack = self.get_object(pk)
            form = PackForm(request.POST, instance=pack)
        else:
            form = PackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('food:pack')
        return render(request, self.template_name, {'form': form})
