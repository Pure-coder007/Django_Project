from functools import wraps
from rest_framework import status
from authentication.models import UserSubscription
from rest_framework.response import Response
from datetime import datetime, timedelta



def handle_unsubscribed_users(view_func):
    @wraps(view_func)
    def wrapper(self, request, *args, **kwargs):
        print(request, "REQUEST")
        user = request.user
        subscription = UserSubscription.objects.filter(
        user=user
        ).order_by('-start_date').first()
        if not subscription:
            return Response({"error": "You are not subscribed to any plan"}, status=status.HTTP_403_FORBIDDEN)
        if subscription.end_date < datetime.now():
            return Response({"error": "Your subscription has expired"}, status=status.HTTP_403_FORBIDDEN)
        return view_func(request, *args, **kwargs)
    return wrapper