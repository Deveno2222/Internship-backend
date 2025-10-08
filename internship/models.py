from django.db import models
from django.conf import settings

# Create your models here.
class Internship(models.Model):
    STATUS_CHOICES = (
        ("open", "Open"),
        ("closed", "Closed"),
        ("in_progress", "In Progress"),
        ("finished", "Finished"),
    )
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")
    created_at = models.DateTimeField(auto_now_add=True)
    
    employer = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="internships"
    )
    
    def __str__(self):
        return f"{self.title} ({self.status})"
    
    
class Application(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )

    internship = models.ForeignKey(
        Internship, 
        on_delete=models.CASCADE, 
        related_name="applications"
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="applications"
    )
    motivation = models.TextField() 
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["internship", "student"], name="unique_application_per_student"
            )
        ]

    def __str__(self):
        return f"{self.student.username} → {self.internship.title} ({self.status})"
