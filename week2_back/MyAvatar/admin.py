from django.contrib import admin
from .models import User
from .models import Expense
from .models import Friend
from .models import Item

# Register your models here.
admin.site.register(User)
admin.site.register(Expense)
admin.site.register(Friend)
admin.site.register(Item)

