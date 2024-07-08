from django.db import models

class User(models.Model):
    login_id = models.CharField(max_length=100, unique=True)
    nickname = models.CharField(max_length=45)
    daily_goal = models.IntegerField(default=0)
    current_potato = models.IntegerField(default=0)

    def __str__(self):
        return self.nickname

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    price = models.IntegerField()

    def __str__(self):
        return f"{self.user.nickname} - {self.price}"

class Friend(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
    are_we_friend = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.from_user.nickname} -> {self.to_user.nickname} : {'Friends' if self.are_we_friend else 'Not Friends'}"

class Item(models.Model):
    name = models.CharField(max_length=45)
    type = models.CharField(max_length=45)
    price = models.IntegerField()
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='items')

    def __str__(self):
        return self.name