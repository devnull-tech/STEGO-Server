from django.contrib import admin
from .models import *

class ContainerAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user']

admin.site.register(Container, ContainerAdmin)
