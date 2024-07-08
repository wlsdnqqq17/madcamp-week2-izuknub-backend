from django.contrib import admin
from .models import User, Friend, Item, UserItem, UserAvatarState

# Register your models here.
admin.site.register(User)
admin.site.register(Friend)
admin.site.register(Item)
admin.site.register(UserItem)
admin.site.register(UserAvatarState)

