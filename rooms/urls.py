from django.urls import path

from chat.views import MessageHistoryView

from .views import (
    AssetListView,
    JoinRoomView,
    LeaveRoomView,
    RoomDetailView,
    RoomListView,
    RoomMembersView,
)
from .market_views import AssetPriceView

urlpatterns = [
    path(
        "assets/",
        AssetListView.as_view(),
        name="asset-list",
    ),

    path(
        "",
        RoomListView.as_view(),
        name="room-list",
    ),

    path(
        "<int:room_id>/",
        RoomDetailView.as_view(),
        name="room-detail",
    ),

    path(
        "<int:room_id>/join/",
        JoinRoomView.as_view(),
        name="room-join",
    ),

    path(
        "<int:room_id>/leave/",
        LeaveRoomView.as_view(),
        name="room-leave",
    ),

    path(
        "<int:room_id>/members/",
        RoomMembersView.as_view(),
        name="room-members",
    ),

    # Message history
    path(
        "<int:room_id>/messages/",
        MessageHistoryView.as_view(),
        name="room-messages",
    ),

    path(
    "assets/<str:symbol>/price/",
    AssetPriceView.as_view(),
    name="asset-price",
    ),
]