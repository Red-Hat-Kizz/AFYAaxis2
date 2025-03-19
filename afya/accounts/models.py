# models.py
from django.db import models
from django.contrib.auth.models import User
import random
import string

def generate_afya_id():
    """Generate a 7-character alphanumeric ID."""
    characters = string.ascii_uppercase + string.digits  # A-Z and 0-9
    while True:
        afya_id = ''.join(random.choice(characters) for _ in range(7))
        if not Profile.objects.filter(afya_id=afya_id).exists():
            return afya_id
        
    return ''.join(random.choice(characters) for _ in range(7))


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    afya_id = models.CharField(max_length=7, unique=True, default=generate_afya_id, editable=False)

    # Personal Information
    date_of_birth = models.DateField(null=True, blank=True)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('P', 'Prefer not to say'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    # Health Information
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES, null=True, blank=True)
    height = models.FloatField(null=True, blank=True, help_text="Height in centimeters")
    weight = models.FloatField(null=True, blank=True, help_text="Weight in kilograms")
    allergies = models.TextField(null=True, blank=True, help_text="List any allergies")
    chronic_conditions = models.TextField(null=True, blank=True, help_text="List any chronic conditions")

    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=100, null=True, blank=True)
    emergency_contact_phone = models.CharField(max_length=15, null=True, blank=True)
    RELATIONSHIP_CHOICES = [
        ('Spouse', 'Spouse'),
        ('Parent', 'Parent'),
        ('Sibling', 'Sibling'),
        ('Child', 'Child'),
        ('Friend', 'Friend'),
        ('Other', 'Other'),
    ]
    emergency_contact_relationship = models.CharField(max_length=50, choices=RELATIONSHIP_CHOICES, null=True, blank=True)

    # Additional Information
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)  # Free-text input
    state = models.CharField(max_length=100, null=True, blank=True)    # Free-text input
    city = models.CharField(max_length=100, null=True, blank=True)     # Free-text input
    postal_code = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"