from rest_framework import serializers

from .models import Asset, Room, RoomMember


class AssetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Asset
        fields = [
            "id",
            "symbol",
            "name",
            "asset_type",
            "is_active",
        ]


class RoomMemberSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        source="user.username",
        read_only=True,
    )

    class Meta:
        model = RoomMember
        fields = [
            "id",
            "username",
            "role",
            "joined_at",
        ]


class RoomSerializer(serializers.ModelSerializer):
    asset = AssetSerializer(
        read_only=True,
    )

    member_count = serializers.IntegerField(
        source="members.count",
        read_only=True,
    )

    class Meta:
        model = Room
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "asset",
            "is_public",
            "member_count",
            "created_at",
        ]