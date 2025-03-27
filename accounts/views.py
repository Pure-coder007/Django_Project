from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.models import User, SubscriptionPlan, UserSubscription, Content, Like, Views
import cloudinary
import cloudinary.uploader
from rest_framework import generics, permissions
from datetime import timedelta, datetime
from django.utils.timezone import now
from authentication.models import Category
import cloudinary.api
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import os
from dotenv import load_dotenv
from dateutil.relativedelta import relativedelta
from .decorators import handle_unsubscribed_users




class GetUserDetails(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self, request):
        user = request.user
        return Response({"user": user.email,
                        "user_id": user.id,
                        "first_name": user.first_name}, status=status.HTTP_200_OK)
    

# Create your views here.


# Get all categories
class GetCategories(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self, request):
        categories = Category.objects.all()
        return Response({"categories": [
            {"id": category.id, "name": category.name} for category in categories]}, status=status.HTTP_200_OK)





class GetSubscriptionPlans(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self, request):
        subscription_plans = SubscriptionPlan.objects.all()
        return Response({"subscription_plans": [
            {"id": subscription_plan.id, "name": subscription_plan.name, "duration": subscription_plan.duration, "price": subscription_plan.price} for subscription_plan in subscription_plans
    ]})
        
        
        

class GetAllContents(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    
    @handle_unsubscribed_users
    def get(self, request):
        contents = Content.objects.all()
        return Response({"contents": [
            {"id": content.id, "title": content.title, "description": content.description, "tags": content.tags, "category": content.category.name} for content in contents
    ]})
        
        
        
        



class SubscribeUser(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        subscription_plan_id = request.data.get('subscription_plan_id')
        if not subscription_plan_id or not str(subscription_plan_id).isdigit():
            return Response(
                {"error": "Valid subscription_plan_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            subscription_plan = SubscriptionPlan.objects.get(id=int(subscription_plan_id))
            UserSubscription.objects.create(
                user=request.user,
                subscription_plan=subscription_plan,
                start_date=datetime.now(),
                end_date=datetime.now() + relativedelta(months=subscription_plan.duration)
            )
            return Response(
                {
                    "message": f"Subscribed successfully to {subscription_plan.name} plan",
                    "details": {
                        "plan_name": subscription_plan.name,
                        "start_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "expiry_date": (datetime.now() + relativedelta(months=subscription_plan.duration)).strftime("%Y-%m-%d %H:%M:%S"),
                        "duration_months": subscription_plan.duration,
                        "price": float(subscription_plan.price)
                    }
                },
                status=status.HTTP_201_CREATED
                )
            
        except SubscriptionPlan.DoesNotExist:
            return Response(
                {"error": "Subscription plan not found"},
                status=status.HTTP_404_NOT_FOUND
            )