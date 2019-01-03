from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import User

from login.models import on_demand_feeds, on_demand_feeds_cta,UserProfile
class UserProfileInline(admin.TabularInline):
    model = UserProfile



class UserAdmin(DjangoUserAdmin):
    inlines = (UserProfileInline,)



admin.site.unregister(User)
admin.site.register(User, UserAdmin)
#admin.site.register(on_demand_feeds)
#admin.site.register(on_demand_feeds_cta)
# Register your models here.
