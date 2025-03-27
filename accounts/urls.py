from django.urls import path
from . import views



urlpatterns = [
    # path("register/", views.register, name="register"),
    path("user_details", views.GetUserDetails.as_view(), name="user_details"),
    path("get_categories", views.GetCategories.as_view(), name="get_categories"),
    path("plans", views.GetSubscriptionPlans.as_view(), name="get_subscription_plans"),
    path("contents", views.GetAllContents.as_view(), name="get_all_contents"),
    path("subscribe", views.SubscribeUser.as_view(), name="subscribe"),

]