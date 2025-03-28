from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import MinLengthValidator
from django.conf import settings
from datetime import datetime


# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("The Email field must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(max_length=225, unique=True)
    username = None
    password = models.CharField(
        max_length=225, validators=[MinLengthValidator(8)], null=False
    )
    first_name = models.CharField(max_length=225, null=False)
    last_name = models.CharField(max_length=225, null=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=225, unique=True)

    def __str__(self):
        return self.name


class Content(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=225, null=False)
    description = models.TextField()
    tags = models.CharField(max_length=225, null=False)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="contents", db_index=True
    )

    views_count = models.IntegerField(default=0)
    likes_count = models.IntegerField(default=0)
    unlikes_count = models.IntegerField(default=0)
    ai_relevance_score = models.FloatField(default=0.0)

    def update_ai_relevance_score(self):
        w1, w2, w3 = 0.2, 1.0, 1.5
        self.ai_relevance_score = (
            (w1 * self.views_count)
            + (w2 * self.likes_count)
            - (w3 * self.unlikes_count)
        )
        self.save()

    def __str__(self):
        return self.title


class Like(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="likes", db_index=True
    )
    content = models.ForeignKey(
        Content, on_delete=models.CASCADE, related_name="likes", db_index=True
    )
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "content")

    def save(self, *args, **kwargs):
        is_new_like = not self.pk
        super().save(*args, **kwargs)
        if is_new_like:
            self.content.likes_count += 1
            self.content.update_ai_relevance_score()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.content.likes_count = max(0, self.content.likes_count - 1)
        self.content.unlikes_count += 1
        self.content.update_ai_relevance_score()


class Views(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="views", db_index=True
    )
    content = models.ForeignKey(
        Content, on_delete=models.CASCADE, related_name="views", db_index=True
    )
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "content")  # Prevent duplicate views

    def save(self, *args, **kwargs):
        """Increase views count and update AI score when content is viewed"""
        is_new_view = not self.pk
        super().save(*args, **kwargs)
        if is_new_view:
            self.content.views_count += 1
            self.content.update_ai_relevance_score()


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    duration = models.IntegerField(null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class UserSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    auto_renewal = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.subscription_plan.name}"
