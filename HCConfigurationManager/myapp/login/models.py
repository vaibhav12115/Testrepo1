from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', related_name='profile')
    #access_rights_number = models.IntegerField()
    privileges = models.CharField(max_length=100)

class on_demand_feeds(models.Model):
    card_title = models.CharField(unique=True, max_length=100)
    deeplink = models.CharField( max_length=100)
    card_sub_title = models.CharField( max_length=100)
    card_start_date = models.DateTimeField()
    card_expiry_date = models.DateTimeField()
    #card_start_date = models.CharField(max_length=100)
    #card_expiry_date = models.CharField(max_length=100)
    card_image = models.CharField( max_length=100)
    priority = models.IntegerField()
    card_icon = models.CharField(max_length=100)
    card_category=models.IntegerField(default=0)
    is_processed=models.IntegerField(default=0)
    created_at=models.DateTimeField(default=datetime.now())
    card_status=models.IntegerField(default=0)

    class Meta:
        db_table = "on_demand_feeds"
        #app_label = 'feeds_data'
    def __unicode__(self):
        return self.card_title



class on_demand_feeds_cta(models.Model):
    feed_id = models.IntegerField()
    link = models.CharField( max_length=100)
    cta_text = models.CharField( max_length=100)
    created_at = models.DateTimeField()
    status = models.IntegerField()
    display_order=models.IntegerField()

    class Meta:
        db_table = "on_demand_feeds_cta"
        #app_label = 'feeds_data'

    def __unicode__(self):
        return self.link

# Create your models here.
