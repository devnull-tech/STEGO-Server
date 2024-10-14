from django.contrib import admin
from .models import *

class ContainerAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user']

class PhotoAdmin(admin.ModelAdmin):
    list_display = ['__str__']

admin.site.register(Container, ContainerAdmin)
admin.site.register(Photo, PhotoAdmin)