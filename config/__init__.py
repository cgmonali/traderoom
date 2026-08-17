from .celery import app as celery_app


__all__ = ("celery_app",)
#So Celery automatically loads when Django loads the project.