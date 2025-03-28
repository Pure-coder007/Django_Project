from functools import wraps
from rest_framework import status
from authentication.models import UserSubscription
from rest_framework.response import Response
from datetime import datetime, timedelta
from django.utils import timezone


def handle_unsubscribed_users(view_func):
    @wraps(view_func)
    def wrapper(self, request, *args, **kwargs):
        user = request.user
        subscription = (
            UserSubscription.objects.filter(user=user).order_by("-start_date").first()
        )

        if not subscription:
            return Response(
                {"error": "You are not subscribed to any plan"},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Compare dates properly (convert datetime to date if needed)
        today = timezone.now().date()  # Get today's date object
        if subscription.end_date < today:
            return Response(
                {"error": "Your subscription has expired"},
                status=status.HTTP_403_FORBIDDEN,
            )

        return view_func(self, request, *args, **kwargs)

    return wrapper


def superuser_required(view_func):
    """Decorator to restrict access to superusers only."""

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response(
                {"error": "Superuser access required"}, status=status.HTTP_403_FORBIDDEN
            )
        return view_func(request, *args, **kwargs)

    return wrapper
