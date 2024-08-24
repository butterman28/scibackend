from django.db import models

# from djmoney.models.fields import *
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

category = (
    ("agriculture", "Agriculture"),
    ("health", "Health"),
    ("climate", "Climate"),
    ("law & order", "Law & Order"),
    ("society", "Society"),
    ("education", "Education"),
    ("politics", "Politics"),
)


class Post(models.Model):
    image = models.ImageField(default="default.jpg", upload_to="img")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(
        max_length=800,
        choices=category,
        blank=True,
        null=True,
    )

    def get_likes(self):
        return self.like_set.all()


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_liked = models.DateTimeField(default=timezone.now)


class Podcast(models.Model):
    image = models.ImageField(default="default.jpg", upload_to="img")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    audio = models.FileField(upload_to="audio/")
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(
        max_length=800,
        choices=category,
        blank=True,
        null=True,
    )

    def get_likes(self):
        return self.podcast_like_set.all()


class Podcast_Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE)
    date_liked = models.DateTimeField(default=timezone.now)


class Podcast_Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    podcast = models.ForeignKey(
        Podcast,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


# Create your models here.
