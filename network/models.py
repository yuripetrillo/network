from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=24)
    content = models.CharField(max_length=64)
    timestamp = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    likes = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.timestamp})"
    pass

class PostLikes(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liker')

    def __str__(self):
        return f"{self.post} ({self.user})"
    pass

class Follow(models.Model):
    id = models.AutoField(primary_key=True)
    follower = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='follower', blank=True, null=True)
    following = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='following', blank=True, null=True)

    def __str__(self):
        return f"{self.follower} follow -> ({self.following})"
    pass
