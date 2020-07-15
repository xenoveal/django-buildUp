from django.db import models
from django.contrib.auth.models import User

class PrivatePost(models.Model):
    username = models.ForeignKey(User, on_delete = models.CASCADE, related_name="posted") #who posted
    paragraph = models.TextField(max_length=300)
    liked = models.ManyToManyField(User, related_name="liked", blank=True) #who like
    bookmarked = models.ManyToManyField(User, related_name="bookmarked", blank=True) #who bookmark
    timestamp = models.DateTimeField(auto_now_add=True)

    def count_liked(self):
        return f"{self.liked.count()}"
    
    def count_comment(self):
        return f"{self.have_comment.count()}"

    def get_comment(self):
        comments = self.have_comment.all()
        return list(comments)

    def __str__(self):
        return f"\"{self.paragraph}\" ({self.username} on {self.timestamp})"

class commentPrivatePost(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commented")
    post = models.ForeignKey(PrivatePost, on_delete = models.CASCADE, related_name="have_comment")
    paragraph = models.TextField(max_length=200)
    commentLike = models.ManyToManyField(User, related_name="liked_comment", blank=True) #who like
    timestamp = models.DateTimeField(auto_now_add=True)

    def count_liked(self):
        return f"{self.commentLike.count()}"
        
    def __str__(self):
        return f"\"{self.paragraph}\" ({self.username} on {self.timestamp})"

class CollaborationPost(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="needColabs")
    title = models.CharField(max_length=100)
    paragraph = models.TextField(max_length=300)
    category = models.CharField(max_length=50)
    members = models.IntegerField()
    location = models.CharField(max_length=50)
    bookmarked = models.ManyToManyField(User, related_name="colabs_bookmarked", blank=True) #who bookmark
    colabs_join = models.ManyToManyField(User, related_name="joined_colabs", blank=True) #who join
    timestamp = models.DateTimeField(auto_now_add=True)

    def count_joined(self):
        return f"{self.colabs_join.count()}"

    def __str__(self):
        return f"{self.title} - {self.paragraph} - {self.category} - {self.members} - {self.location} ======== posted by: {self.username}"

class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name}"

class Content(models.Model):
    title = models.CharField(max_length=100)
    paragraph = models.TextField(max_length=1000)
    terms = models.TextField(max_length=1000)
    username = models.ForeignKey(User, on_delete = models.CASCADE, related_name="added") #who posted
    bookmarked = models.ManyToManyField(User, related_name="info_bookmarked", blank=True) #who bookmark
    contentImage = models.ImageField(blank=True, upload_to="galery")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="have_content")
    held_on_start = models.DateTimeField()
    held_on_end = models.DateTimeField()
    max_participants = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    guidebook = models.CharField(max_length=100, blank=True)
    teams = models.ManyToManyField(CollaborationPost, blank=True, related_name="for_joined")

    def __str__(self):
        return f"{self.title} - {self.category.name} ======== {self.paragraph}"