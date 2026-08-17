from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rooms.models import Room, RoomMember

from .models import Message
from .serializers import MessageSerializer







class MessageHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, room_id):

        room = Room.objects.get(
            id=room_id
        )

        is_member = RoomMember.objects.filter(
            room=room,
            user=request.user,
        ).exists()

        if not is_member:
            return Response(
                {
                    "error": "You are not a member of this room."
                },
                status=403,
            )

        messages = (
            Message.objects
            .filter(room=room)
            .select_related("user")
            .order_by("created_at")
        )

        serializer = MessageSerializer(
            messages,
            many=True,
        )

        return Response(serializer.data)