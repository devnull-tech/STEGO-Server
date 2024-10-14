from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, APIKey

class CustomUserAdmin(UserAdmin):
    def generate_keys(self, request, queryset):
        for user in queryset:
            user.generate_api_key()
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_pgp_public_key',)}),
    )
    actions = [generate_keys]

class APIKeyAdmin(admin.ModelAdmin):
    list_display = ['user', 'key']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(APIKey, APIKeyAdmin)
