from django.contrib import admin
from django.contrib.auth.models import Group
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

from users.models import User, Tier

admin.site.register(User)
admin.site.register(Tier)

admin.site.unregister(Group)
admin.site.unregister(BlacklistedToken)
admin.site.unregister(OutstandingToken)
