from django.contrib import admin
from .models import *
# Register your models here.
class LocationAdmin(admin.ModelAdmin):
    list_display = ['id', 'longitude', 'latitude']

admin.site.register(Location, LocationAdmin)