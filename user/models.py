import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    user_pgp_public_key = models.TextField(blank=True, null=True)

    def generate_api_key(self) -> None:
        api_key, created = APIKey.objects.get_or_create(user=self)
        if not created:
            api_key.key = uuid.uuid4()
            api_key.save()

class APIKey(models.Model):
    key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
