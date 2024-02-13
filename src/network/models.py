from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.CharField(max_length = 180)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.creator} created {self.content}"

    class Meta:
        ordering = ["-created"]

class SocialSystem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    following_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    created = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id','following_user_id'],  name="unique_followers")
        ]
        ordering = ['-created']

    def __str__(self) -> str:
        return f"{self.user} followed {self.following_user}"
    
class LikeSystem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liked")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="p_status")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id','post_id'],  name="unique_likes")
        ]

    def __str__(self) -> str:
            return f"{self.user} liked {self.post}"
