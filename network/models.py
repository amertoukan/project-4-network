from django.contrib.auth.models import AbstractUser
from django.core.exceptions import MiddlewareNotUsed
from django.db import models

from django.db.models.fields.related import ForeignKey, ManyToManyField

class User(AbstractUser):
    pass

class Follow(models.Model): 
    user = ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    following = ForeignKey(User, on_delete=models.CASCADE, related_name="following")

    def __str__(self): 
        return f"{self.user} follows {self.following}"

class Post (models.Model): 
    id = id
    poster = ForeignKey(User, on_delete=models.CASCADE, related_name="creator_of_post")
    content = models.TextField(max_length=140)
    created = models.DateTimeField(auto_now_add=True)
    likes = ManyToManyField(User, blank=True)


    def __str__(self):
        return f"{self.poster}: {self.content}"

    