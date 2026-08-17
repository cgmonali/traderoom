from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Asset, Room, RoomMember
from .serializers import (
    AssetSerializer,
    RoomMemberSerializer,
    RoomSerializer,
)


class AssetListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        assets = Asset.objects.filter(
            is_active=True
        )

        serializer = AssetSerializer(
            assets,
            many=True,
        )

        return Response(serializer.data)


class RoomListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rooms = (
            Room.objects
            .filter(is_public=True)
            .select_related("asset", "created_by")
        )

        serializer = RoomSerializer(
            rooms,
            many=True,
        )

        return Response(serializer.data)

    @transaction.atomic
    def post(self, request):
        symbol = request.data.get("symbol")
        name = request.data.get("name")
        description = request.data.get(
            "description",
            "",
        )

        if not symbol or not name:
            return Response(
                {
                    "error": "symbol and name are required"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        asset = get_object_or_404(
            Asset,
            symbol=symbol.upper(),
            is_active=True,
        )

        if Room.objects.filter(
            asset=asset
        ).exists():
            return Response(
                {
                    "error": "A room already exists for this asset."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        slug = symbol.lower()

        room = Room.objects.create(
            name=name,
            slug=slug,
            description=description,
            asset=asset,
            created_by=request.user,
        )

        RoomMember.objects.create(
            room=room,
            user=request.user,
            role=RoomMember.Role.OWNER,
        )

        serializer = RoomSerializer(room)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class RoomDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, room_id):
        room = get_object_or_404(
            Room.objects.select_related("asset"),
            id=room_id,
        )

        serializer = RoomSerializer(room)

        return Response(serializer.data)


class JoinRoomView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, room_id):
        room = get_object_or_404(
            Room,
            id=room_id,
        )

        membership, created = RoomMember.objects.get_or_create(
            room=room,
            user=request.user,
            defaults={
                "role": RoomMember.Role.MEMBER,
            },
        )

        if not created:
            return Response(
                {
                    "message": "You are already a member of this room."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = RoomMemberSerializer(
            membership
        )

        return Response(
            {
                "message": "Joined room successfully",
                "membership": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


class LeaveRoomView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, room_id):
        room = get_object_or_404(
            Room,
            id=room_id,
        )

        membership = get_object_or_404(
            RoomMember,
            room=room,
            user=request.user,
        )

        if membership.role == RoomMember.Role.OWNER:
            return Response(
                {
                    "error": "Room owner cannot leave the room."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        membership.delete()

        return Response(
            {
                "message": "Left room successfully"
            }
        )


class RoomMembersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, room_id):
        room = get_object_or_404(
            Room,
            id=room_id,
        )

        members = (
            RoomMember.objects
            .filter(room=room)
            .select_related("user")
        )

        serializer = RoomMemberSerializer(
            members,
            many=True,
        )

        return Response(serializer.data)