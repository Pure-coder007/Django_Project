from django.utils import timezone
from dateutil.relativedelta import relativedelta
from celery import shared_task

from celery import shared_task
from django.utils.timezone import now, timedelta
from authentication.models import Like, Views
from authentication.models import Content


@shared_task
def renew_expired_subscriptions():
    now = timezone.now()

    print("Checking for expired subscriptions...")

    expired_subs = UserSubscription.objects.filter(
        end_date__lte=now,
        auto_renewal=True,
    ).select_related("subscription_plan")

    for old_sub in expired_subs:
        print(f"Renewing subscription for user {old_sub.user.last_name}")
        UserSubscription.objects.create(
            user=old_sub.user,
            subscription_plan=old_sub.subscription_plan,
            start_date=now,
            end_date=now + relativedelta(months=old_sub.subscription_plan.duration),
            auto_renewal=old_sub.auto_renewal,
        )

    return True


@shared_task
def calculate_ai_relevance_scores():
    all_content = Content.objects.all()

    for content in all_content:
        one_week_ago = now() - timedelta(days=7)

        likes_count = Like.objects.filter(
            content=content, created_at__gte=one_week_ago
        ).count()
        views_count = Views.objects.filter(
            content=content, viewed_at__gte=one_week_ago
        ).count()

        ai_score = (likes_count * 2) + (views_count * 1)

        content.ai_relevance_score = ai_score
        content.save()

    return f"Updated AI relevance scores for {all_content.count()} content items."
