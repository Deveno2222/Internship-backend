from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    ROLES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('employer', 'Employer'),
    ]
    
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLES)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username"]
    
    def __str__(self):
        return self.email