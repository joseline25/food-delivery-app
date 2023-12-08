from django import forms
from .models import *
from django.core.exceptions import ValidationError

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
        
        
        
class OpeningHourForm(forms.ModelForm):
    WEEKDAY_CHOICES = [
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
        (7, 'Sunday'),
    ]
    weekday = forms.ChoiceField(choices=WEEKDAY_CHOICES)
    
    # validator to make sure that open_time is earlier than close_time
    def clean(self):
        cleaned_data = super().clean()
        open_time = cleaned_data.get('open_time')
        close_time = cleaned_data.get('close_time')

        if open_time and close_time and open_time >= close_time:
            raise ValidationError("Closing time must be later than opening time.")
        
        """ 
The clean method accesses the form's cleaned_data dictionary, which contains
the validated form field values.
We check if both the open_time and close_time fields are present and compare them.
If the close_time is earlier than or equal to the open_time, we raise a
ValidationError with a specified error message.
This validation ensures that the closing time cannot be set to a time earlier than the opening time.

"""
        

    class Meta:
        model=OpeningHour
        exclude=['restaurant']
        widgets={
            
            
            'open_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'close_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            
            
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