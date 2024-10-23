from django.contrib import admin

from .models import User, GlobalMessage, Friends, ProfilePic, Direct, DirectMessage, Group, GroupMessage, GroupInvite

# Register your models here.

admin.site.register(User)
admin.site.register(GlobalMessage)
admin.site.register(Friends)
admin.site.register(ProfilePic)
admin.site.register(Direct)
admin.site.register(DirectMessage)
admin.site.register(Group)
admin.site.register(GroupMessage)
admin.site.register(GroupInvite)