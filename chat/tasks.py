from celery import shared_task


@shared_task
def analyze_message(message_id):

    from .models import Message 
    #This keeps task discovery/imports cleaner and avoids unnecessary model loading while Celery initializes.

    message = Message.objects.get(
        id=message_id
    )

    content = message.content.lower()

    if any(
        word in content
        for word in [
            "bullish",
            "buy",
            "long",
            "pump",
            "up",
        ]
    ):
        sentiment = "BULLISH"

    elif any(
        word in content
        for word in [
            "bearish",
            "sell",
            "short",
            "dump",
            "down",
        ]
    ):
        sentiment = "BEARISH"

    else:
        sentiment = "NEUTRAL"

    print(
        f"Message {message.id}: {sentiment}"
    )

    return {
        "message_id": message.id,
        "sentiment": sentiment,
    }