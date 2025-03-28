from django.urls import path
from . import views


urlpatterns = [
    path("user_details", views.GetUserDetails.as_view(), name="user_details"),
    path("get_categories", views.GetCategories.as_view(), name="get_categories"),
    path("plans", views.GetSubscriptionPlans.as_view(), name="get_subscription_plans"),
    path("contents", views.GetAllContents.as_view(), name="get_all_contents"),
    path("subscribe", views.SubscribeUser.as_view(), name="subscribe"),
    path(
        "single_content/<int:content_id>/",
        views.GetSingleContent.as_view(),
        name="single_content",
    ),
    path(
        "content/<int:content_id>/like",
        views.LikeContent.as_view(),
        name="like-content",
    ),
    path("recommendation", views.RecommendContent.as_view(), name="recommendation"),
    path("add_content", views.AddContent.as_view(), name="add_content"),
    path("add_category", views.AddCategory.as_view(), name="add_category"),
]
