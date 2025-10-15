from django.db.models.signals import post_save
from .models import User , Profile

def create_profile_user(sender , *args , **kwargs):
    if kwargs['created']:
        Profile.objects.create(user = kwargs['instance'])
post_save.connect(sender=User , receiver=create_profile_user)