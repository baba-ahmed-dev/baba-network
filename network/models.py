from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    pass

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    img = models.ImageField(upload_to="photos%d%y%m", default="defaultProfile.png",null=True , blank=True)
    description = models.TextField(max_length=200 , null=True, blank=True)
    
    
    
    def __str__(self):
        return str(self.user)

@receiver(post_save, sender=User)
def create_user_profile(sender,instance,created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance
        )

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.TextField(max_length=200)
    date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-date"]
        
    def __str__(self):
        return str(f'{self.user} post')

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment")
    post = models.ForeignKey(Post, on_delete=models.CASCADE , related_name="post_comments")
    body = models.TextField(max_length=400)
    date = models.DateTimeField(auto_now=True)

    
    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.user} commnted on {self.post} ."

class Follow(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE , related_name="followings")
    followed = models.ForeignKey(User, on_delete=models.CASCADE , related_name="followeds")
    val = models.BooleanField(default=False)
     
    def __str__(self):
        return f"{self.following} following {self.followed} ."

class Like(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE ,related_name="user_likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE , related_name="post_likes")
    
    def __str__(self):
        return f"{self.user} liked {self.post} ."
