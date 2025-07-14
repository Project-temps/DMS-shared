from django.db import models

from django.contrib.auth.models import User

class Profile(models.Model):
    USER_GROUP_CHOICES = [
        ("farmer", "Farmer"),
        ("consumer", "Consumer"),
        ("stakeholder", "Stakeholder"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.CharField(max_length=20, choices=USER_GROUP_CHOICES)
    country = models.CharField(max_length=100, blank=True)
    farm_address = models.TextField(blank=True)

    # Add more fields here if needed
    def __str__(self):
        return f"{self.user.username} ({self.group})"
