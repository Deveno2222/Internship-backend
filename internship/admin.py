from django.contrib import admin
from .models import Internship, Application
# Register your models here.
@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
    list_display = ("title", "employer", "location", "status", "created_at")
    list_filter = ("status", "location")
    search_fields = ("title", "description", "location", "employer__username")
    ordering = ("-created_at",)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("internship", "student", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("internship__title", "student__username", "motivation")
    ordering = ("-created_at",)