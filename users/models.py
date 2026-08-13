from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        unique=True
    )
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True,
    )
    reputation = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username