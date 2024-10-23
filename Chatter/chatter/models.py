from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    bio = models.CharField(max_length = 1000, default = '')

class ProfilePic(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to = 'chatter/static/chatter/profile_picture', blank = True)


class Friends(models.Model):
    follower = models.ForeignKey(User, related_name = "follow", on_delete = models.CASCADE)
    following = models.ForeignKey(User, related_name = "followed", on_delete = models.CASCADE)

class Direct(models.Model):
    friend_1 = models.ForeignKey(User, related_name = "friend_1", on_delete = models.CASCADE)
    friend_2 = models.ForeignKey(User, related_name = "friend_2", on_delete = models.CASCADE)

class Group(models.Model):
    group_name = models.CharField(max_length = 1000)
    owner = models.ForeignKey(User, related_name = "group_owner", on_delete = models.CASCADE)
    description = models.CharField(max_length = 10000)
    category = models.CharField(max_length = 1000, default = "General")
    members = models.ManyToManyField(User, related_name = "joined_group")

class GroupMessage(models.Model):
    group = models.ForeignKey(Group, related_name = "group", on_delete = models.CASCADE)
    content = models.CharField(max_length = 1000)
    date = models.DateField(auto_now = True)
    messager = models.ForeignKey(User, related_name = "user_group", on_delete = models.CASCADE)
    likes = models.ManyToManyField(User, related_name = "likes_group")
    reply = models.CharField(max_length = 1000, blank = True)
    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "date": self.date,
            "messager": self.messager.username,
            "likes": self.likes.count(),
            "reply": self.reply,          
        }

class GroupInvite(models.Model):
    group = models.ForeignKey(Group, related_name = "group_invite", on_delete = models.CASCADE)
    user = models.ForeignKey(User, related_name = "invitee", on_delete = models.CASCADE)

class DirectMessage(models.Model):
    direct = models.ForeignKey(Direct, related_name = "friends", on_delete = models.CASCADE)
    content = models.CharField(max_length = 1000)
    date = models.DateField(auto_now = True)
    messager = models.ForeignKey(User, related_name = "user_direct", on_delete = models.CASCADE)
    likes = models.ManyToManyField(User, related_name = "likes_direct")
    reply = models.CharField(max_length = 1000, blank = True)
    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "date": self.date,
            "messager": self.messager.username,
            "likes": self.likes.count(),
            "reply": self.reply,

            
        }

class GlobalMessage(models.Model):
    content = models.CharField(max_length = 1000)
    date = models.DateField(auto_now = True)
    messager = models.ForeignKey(User, related_name = "user", on_delete = models.CASCADE)
    likes = models.ManyToManyField(User, related_name = "likes")
    reply = models.CharField(max_length = 1000, blank = True)
    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "date": self.date,
            "messager": self.messager.username,
            "likes": self.likes.count(),
            "reply": self.reply,

            
        }
    



