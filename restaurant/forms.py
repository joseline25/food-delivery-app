from django import forms
from .models import *


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Restaurant name'}),
            'description': forms.Textarea(),
            'rating': forms.NumberInput(attrs={'class': 'form-control'}),
            'location': forms.Select(attrs={'class': 'form-control'}),
            'cuisines': forms.CheckboxSelectMultiple(),
            'category': forms.CheckboxSelectMultiple(),
            'menus': forms.CheckboxSelectMultiple(),
        }
        
        

class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Restaurant name'}),
            'description': forms.Textarea(),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'ingredients': forms.CheckboxSelectMultiple(),
            'categories': forms.CheckboxSelectMultiple(),
            
        }
        
        

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = '__all__'
        


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'