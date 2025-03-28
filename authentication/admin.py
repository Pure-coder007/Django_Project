from django.contrib import admin
from .models import (
    User,
    Category,
    Content,
    Like,
    Views,
    SubscriptionPlan,
    UserSubscription,
)

# Register your models here.

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Content)
admin.site.register(Like)
admin.site.register(Views)
admin.site.register(SubscriptionPlan)
admin.site.register(UserSubscription)
