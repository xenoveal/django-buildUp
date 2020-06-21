from django.db import models
from django.contrib.auth.models import User

class PrivatePost(models.Model):
    username = models.ForeignKey(User, on_delete = models.CASCADE, related_name="posted") #who posted
    paragraph = models.CharField(max_length=300)
    liked = models.ManyToManyField(User, related_name="liked", blank=True) #who like
    timestamp = models.DateTimeField(auto_now_add=True)

    def count_liked(self):
        return f"{self.liked.count()}"

    def __str__(self):
        return f"\"{self.paragraph}\" ({self.username} on {self.timestamp})"

class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name}"

class Content(models.Model):
    title = models.CharField(max_length=100)
    paragraph = models.CharField(max_length=1000)
    username = models.ForeignKey(User, on_delete = models.CASCADE, related_name="added") #who posted
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="content_inside")
    held_on = models.DateTimeField()
    max_participants = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    join = models.ManyToManyField(User, related_name="joined", blank=True)

    def __str__(self):
        return f"{self.title} - {self.category.name} ======== {self.paragraph}"
