from django.db import models
from django.utils import timezone
from django.utils.timezone import localtime

class Service(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='service_images/', blank=True, null=True)
    
    def __str__(self):
        return self.name

class Clinic(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.TextField()
    
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    # Many-to-Many relationship with Service
    services = models.ManyToManyField(Service, related_name='clinics')

    # Clinic images
    image1 = models.ImageField(upload_to='clinic_images/', blank=True, null=True)
    image2 = models.ImageField(upload_to='clinic_images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='clinic_images/', blank=True, null=True)

    def get_current_day_hours(self):
        """Retrieve today's opening hours"""
        current_day = timezone.localtime().strftime('%A')
        print(f"Checking hours for: {current_day}")  # Debugging
        hours = self.opening_hours.filter(day=current_day).first()
        if hours:
            print(f"Opening: {hours.opening_time}, Closing: {hours.closing_time}")  # Debugging
            return {'open': hours.opening_time, 'close': hours.closing_time}
        print("No hours found!")  # Debugging
        return {'open': None, 'close': None}
    
    def is_open_now(self):
        """Check if the clinic is currently open based on local time"""
        current_day_hours = self.get_current_day_hours()
        if current_day_hours['open'] and current_day_hours['close']:
            now = localtime().time()  # Get local time instead of UTC
            return current_day_hours['open'] <= now <= current_day_hours['close']
        return False

    def __str__(self):
        return self.name

class OpeningHours(models.Model):
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name="opening_hours")
    day = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    opening_time = models.TimeField()
    closing_time = models.TimeField()

    class Meta:
        unique_together = ('clinic', 'day')  # Prevent duplicate day entries per clinic

    def __str__(self):
        return f"{self.clinic.name} - {self.day}: {self.opening_time} to {self.closing_time}"
