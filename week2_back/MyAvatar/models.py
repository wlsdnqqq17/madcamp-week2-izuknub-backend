from django.db import models

class User(models.Model):
    login_id = models.CharField(max_length=100, unique=True)
    nickname = models.CharField(max_length=45)

    def __str__(self):
        return self.nickname

class Friend(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
    are_we_friend = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.from_user.nickname} -> {self.to_user.nickname} : {'Friends' if self.are_we_friend else 'Not Friends'}"

class Item(models.Model):
    CATEGORY_CHOICES = [
        ('hat', 'Hat'),
        ('clothes', 'Clothes'),
        ('accessory', 'Accessory'),
        ('background', 'Background')
    ]

    name = models.CharField(max_length=255)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, null=True, blank=True)
    item_image_url = models.CharField(max_length=255, null=True, blank=True)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class UserItem(models.Model):
    user_id = models.ForeignKey(User, related_name='UserItem_UserId', on_delete=models.CASCADE)
    item_id = models.ForeignKey(Item, related_name='UserItem_ItemId', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user_id}: {self.item_id}"

class UserAvatarState(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    hat_item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True, related_name='hat_user')
    clothes_item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True, related_name='clothes_user')
    accessory_item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True, related_name='accessory_user')
    background_item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True, related_name='background_user')

    def __str__(self):
        return f"AvatarState for user {self.user.username}"


