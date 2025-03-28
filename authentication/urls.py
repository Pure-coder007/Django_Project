from django.urls import path
from . import views


urlpatterns = [
    path("login", views.LoginView.as_view(), name="login"),
    path("login_superuser", views.LoginSuperuser.as_view(), name="login_superuser"),
    path("register", views.RegisterUserView.as_view(), name="register"),
    path(
        "register_superuser",
        views.RegisterSuperuserView.as_view(),
        name="register_superuser",
    ),
]
