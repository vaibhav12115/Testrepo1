from django.db.models import signals
from accounts.models import UserProfile
from django.contrib.auth.models import User

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)



signals.post_save.connect(create_user_profile, sender=User)