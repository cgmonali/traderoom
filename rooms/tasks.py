import random
from decimal import Decimal

from celery import shared_task
from django.core.cache import cache

from .models import Asset, AssetPrice


@shared_task
def update_market_prices():

    assets = Asset.objects.filter(
        is_active=True
    )

    updated = []

    for asset in assets:

        latest_price = (
            AssetPrice.objects
            .filter(asset=asset)
            .first()
        )

        if latest_price:
            previous_price = latest_price.price
        else:
            previous_price = Decimal(
                random.uniform(50, 50000)
            )

        change_percent = Decimal(
            str(
                random.uniform(
                    -3,
                    3,
                )
            )
        )

        new_price = previous_price * (
            Decimal("1")
            + change_percent / Decimal("100")
        )

        new_price = new_price.quantize(
            Decimal("0.00000001")
        )

        price = AssetPrice.objects.create(
            asset=asset,
            price=new_price,
            change_percent=change_percent,
        )

        cache.set(
            f"asset_price:{asset.id}",
            {
                "symbol": asset.symbol,
                "price": str(price.price),
                "change_percent": str(
                    price.change_percent
                ),
                "created_at": (
                    price.created_at.isoformat()
                ),
            },
            timeout=60,
        )

        updated.append(
            asset.symbol
        )

    return {
        "updated_assets": updated
    }