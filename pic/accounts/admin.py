from django.contrib import admin
from accounts.models import userprofile,adminuser,notify,adminnotify,subadminuser,AccessToken

# Register your models here.
admin.site.register(userprofile)
admin.site.register(adminuser)
admin.site.register(notify)
admin.site.register(adminnotify)
admin.site.register(subadminuser)
admin.site.register(AccessToken)