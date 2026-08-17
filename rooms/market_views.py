from django.core.cache import cache

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Asset


class AssetPriceView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, symbol):

        asset = Asset.objects.filter(
            symbol=symbol.upper(),
            is_active=True,
        ).first()

        if not asset:
            return Response(
                {
                    "error": "Asset not found"
                },
                status=404,
            )

        cached_price = cache.get(
            f"asset_price:{asset.id}"
        )

        if not cached_price:
            return Response(
                {
                    "error": "Price data unavailable"
                },
                status=404,
            )

        return Response(
            cached_price
        )