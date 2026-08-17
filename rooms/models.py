from django.conf import settings
from django.db import models


class Asset(models.Model):
    class AssetType(models.TextChoices):
        STOCK = "STOCK", "Stock"
        CRYPTO = "CRYPTO", "Crypto"

    symbol = models.CharField(
        max_length=20,
        unique=True,
    )

    name = models.CharField(
        max_length=100,
    )

    asset_type = models.CharField(
        max_length=20,
        choices=AssetType.choices,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.symbol

class AssetPrice(models.Model):

    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name="prices",
    )

    price = models.DecimalField(
        max_digits=20,
        decimal_places=8,
    )

    change_percent = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=0,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.asset.symbol}: {self.price}"



class Room(models.Model):
    name = models.CharField(
        max_length=100,
    )

    slug = models.SlugField(
        max_length=100,
        unique=True,
    )

    description = models.TextField(
        blank=True,
    )

    asset = models.OneToOneField(
        Asset,
        on_delete=models.CASCADE,
        related_name="room",
    )

    is_public = models.BooleanField(
        default=True,
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_rooms",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.name


class RoomMember(models.Model):
    class Role(models.TextChoices):
        OWNER = "OWNER", "Owner"
        MODERATOR = "MODERATOR", "Moderator"
        MEMBER = "MEMBER", "Member"

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="members",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="room_memberships",
    )

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.MEMBER,
    )

    joined_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["room", "user"],
                name="unique_room_member",
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.room.name}"