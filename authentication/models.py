from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.contrib.gis.db import models
from restaurant.models import Restaurant

# Create your models here.


""" 
Identify User Types:

Define the different user roles in your food delivery app, 
such as customers, delivery drivers,  restaurant staff and the superadmin.

Create User Models:

- Extend the default Django User model or create separate models for each user type.
    You can use the AbstractUser class for customization.
"""

class Customer(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True)
    favorite_restaurants = models.ManyToManyField(Restaurant, related_name='favorite_customers', blank=True)

    class Meta:
        permissions = (
            ("can_do_something", "Can do something"),
            # Add more permissions as needed
        )
    
    def __str__(self):
        return self.username

Customer._meta.get_field('groups').related_name = 'customer_groups'
Customer._meta.get_field('user_permissions').related_name = 'customer_user_permissions'


class DeliveryDriver(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    vehicle_type = models.CharField(max_length=50, blank=True)
    vehicle_plate_number = models.CharField(max_length=20, blank=True)
    #  for storing point coordinates
    current_location = models.PointField(null=True, blank=True)  # Requires GeoDjango if using spatial data
    availability_status = models.BooleanField(default=True)
    
    class Meta:
        permissions = (
            ("can_deliver", "Can deliver"),
            # Add more permissions as needed
        )

    def __str__(self):
        return self.username
# Specify a unique related_name for the groups field
DeliveryDriver._meta.get_field('groups').related_name = 'delivery_driver_groups'    

# Specify a unique related_name for the user_permissions field
DeliveryDriver._meta.get_field('user_permissions').related_name = 'delivery_driver_user_permissions'
  
"""  
phone_number: A field to store the delivery driver's phone number.
vehicle_type: A field to specify the type of vehicle the delivery driver uses
(e.g., car, bike).
vehicle_plate_number: A field to store the license plate number of the delivery 
driver's vehicle.
current_location: A spatial field (requires GeoDjango) to store the real-time 
location of the delivery driver.
availability_status: A boolean field indicating whether the delivery driver is 
currently available for deliveries.
Again, customize these fields based on your specific requirements and the features
you want to offer in your food delivery app. If you are using spatial fields like
PointField, make sure to set up GeoDjango in your project.

"""

class RestaurantStaff(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='staff_members')
    role = models.CharField(max_length=50, blank=True)
    shift_start_time = models.TimeField(blank=True, null=True)
    shift_end_time = models.TimeField(blank=True, null=True)
    
    
    class Meta:
        permissions = (
            ("can_do_something", "Can do something"),
            # Add more permissions as needed
        )
    
 
    def __str__(self):
        return self.username
    

 
RestaurantStaff._meta.get_field('groups').related_name = 'restaurant_staff_groups'  
RestaurantStaff._meta.get_field('user_permissions').related_name = 'restaurant_staff_user_permissions'     
    
""" 
phone_number: A field to store the phone number of the restaurant staff member.
restaurant: A foreign key relationship to the Restaurant model, indicating the 
restaurant to which the staff member is associated.
role: A field to specify the role or position of the staff member within the
restaurant (e.g., manager, chef, waiter).
shift_start_time: A field to store the start time of the staff member's shift.
shift_end_time: A field to store the end time of the staff member's shift.
Adjust these fields based on your specific requirements and the information 
you need to manage for restaurant staff members in your food delivery app. 
If you don't have a Restaurant model yet, make sure to define it or adjust the
restaurant field accordingly based on your actual model structure.
"""

class Admin(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    job_title = models.CharField(max_length=255, blank=True)
    
    class Meta:
        permissions = (
            ("can_manage_users", "Can manage users"),
            # Add more permissions as needed
        )



    def __str__(self):
        return self.username
    

# Specify unique related_names for permissions and groups
Admin._meta.get_field('user_permissions').related_name = 'admin_user_permissions'
Admin._meta.get_field('groups').related_name = 'admin_groups'
    
""" 
After defining the Admin model, make sure to update your settings.py to
use this custom user model:

# settings.py

AUTH_USER_MODEL = 'your_app.Admin'
"""