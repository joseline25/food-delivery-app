from django import forms
from .models import Food

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
        
        
