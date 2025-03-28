from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import F, Subquery, OuterRef
from django.core.cache import cache
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.models import (
    User,
    SubscriptionPlan,
    UserSubscription,
    Content,
    Like,
    Views,
)
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
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator

from django.utils import timezone
from dotenv import load_dotenv
from dateutil.relativedelta import relativedelta
from .decorators import handle_unsubscribed_users, superuser_required


# Add categories by superuser
class AddCategory(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(superuser_required)
    def post(self, request):
        name = request.data.get("name")
        if not name:
            return Response(
                {"error": "Category name is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        category = Category.objects.create(name=name)
        return Response(
            {
                "message": "Category added successfully",
                "category": {"id": category.id, "name": category.name},
            },
            status=status.HTTP_201_CREATED,
        )


class AddContent(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(superuser_required)
    def post(self, request):
        title = request.data.get("title")
        description = request.data.get("description")
        tags = request.data.get("tags")
        category_id = request.data.get("category_id")

        if not title:
            return Response(
                {"error": "Title is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        if not description:
            return Response(
                {"error": "Description is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        if not tags:
            return Response(
                {"error": "Tags are required"}, status=status.HTTP_400_BAD_REQUEST
            )
        if not category_id:
            return Response(
                {"error": "Category ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        category = get_object_or_404(Category, id=category_id)
        content = Content.objects.create(
            title=title, description=description, tags=tags, category=category
        )

        return Response(
            {
                "message": "Content added successfully",
                "content": {
                    "id": content.id,
                    "title": content.title,
                    "description": content.description,
                    "tags": content.tags,
                    "category": content.category.name,
                },
            },
            status=status.HTTP_201_CREATED,
        )


class GetUserDetails(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response(
            {"user": user.email, "user_id": user.id, "first_name": user.first_name},
            status=status.HTTP_200_OK,
        )


# Create your views here.


# Get all categories
class GetCategories(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = Category.objects.all()
        return Response(
            {
                "categories": [
                    {"id": category.id, "name": category.name}
                    for category in categories
                ]
            },
            status=status.HTTP_200_OK,
        )


class GetSubscriptionPlans(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        subscription_plans = SubscriptionPlan.objects.all()
        return Response(
            {
                "subscription_plans": [
                    {
                        "id": subscription_plan.id,
                        "name": subscription_plan.name,
                        "duration": subscription_plan.duration,
                        "price": subscription_plan.price,
                    }
                    for subscription_plan in subscription_plans
                ]
            }
        )


class GetAllContents(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @handle_unsubscribed_users
    def get(self, request):
        contents = Content.objects.all()
        return Response(
            {
                "contents": [
                    {
                        "id": content.id,
                        "title": content.title,
                        "description": content.description,
                        "tags": content.tags,
                        "category": content.category.name,
                    }
                    for content in contents
                ]
            }
        )


class SubscribeUser(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        subscription_plan_id = request.data.get("subscription_plan_id")
        if not subscription_plan_id or not str(subscription_plan_id).isdigit():
            return Response(
                {"error": "Valid subscription_plan_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            subscription_plan = SubscriptionPlan.objects.get(
                id=int(subscription_plan_id)
            )
            UserSubscription.objects.create(
                user=request.user,
                subscription_plan=subscription_plan,
                start_date=datetime.now(),
                end_date=datetime.now()
                + relativedelta(months=subscription_plan.duration),
            )
            return Response(
                {
                    "message": f"Subscribed successfully to {subscription_plan.name} plan",
                    "details": {
                        "plan_name": subscription_plan.name,
                        "start_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "expiry_date": (
                            datetime.now()
                            + relativedelta(months=subscription_plan.duration)
                        ).strftime("%Y-%m-%d %H:%M:%S"),
                        "duration_months": subscription_plan.duration,
                        "price": float(subscription_plan.price),
                    },
                },
                status=status.HTTP_201_CREATED,
            )

        except SubscriptionPlan.DoesNotExist:
            return Response(
                {"error": "Subscription plan not found"},
                status=status.HTTP_404_NOT_FOUND,
            )


# Get single content
class GetSingleContent(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, content_id):
        user = request.user
        content = get_object_or_404(Content, id=content_id)

        view, created = Views.objects.get_or_create(user=user, content=content)

        return Response(
            {
                "id": content.id,
                "title": content.title,
                "description": content.description,
                "tags": content.tags,
                "category": content.category.name,
            }
        )


# Like a content
class LikeContent(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, content_id):
        user = request.user
        content = get_object_or_404(Content, id=content_id)
        like, created = Like.objects.get_or_create(user=user, content=content)

        if not created:
            like.delete()
            return Response(
                {"message": "Content unliked successfully"}, status=status.HTTP_200_OK
            )

        return Response(
            {"message": "Content liked successfully"}, status=status.HTTP_201_CREATED
        )


class RecommendContent(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        liked_content_categories = list(
            Like.objects.filter(user=user).values_list("content__category", flat=True)
        )

        viewed_content_categories = list(
            Views.objects.filter(user=user).values_list("content__category", flat=True)
        )

        categories = set(liked_content_categories + viewed_content_categories)

        liked_content_ids = list(
            Like.objects.filter(user=user).values_list("content_id", flat=True)
        )
        viewed_content_ids = list(
            Views.objects.filter(user=user).values_list("content_id", flat=True)
        )
        interacted_content_ids = set(liked_content_ids + viewed_content_ids)

        recommended_content = (
            Content.objects.filter(category__in=categories)
            .exclude(id__in=interacted_content_ids)
            .order_by("-ai_relevance_score")[:5]
        )

        recommendations = [
            {
                "id": content.id,
                "title": content.title,
                "description": content.description,
                "tags": content.tags,
                "category": content.category.name,
                "ai_relevance_score": content.ai_relevance_score,
            }
            for content in recommended_content
        ]

        return Response(
            {
                "recommendations": recommendations,
                "message": "Here are your recommended contents based on your history.",
            },
            status=status.HTTP_200_OK,
        )
