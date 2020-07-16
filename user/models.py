from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserExtend(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    verified = models.BooleanField(default=False)
    profileImg = models.ImageField(blank=True, upload_to="galery")

    def __str__(self):
        return f"Extended information for {self.user}'"

class Token(models.Model):
    token = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='have_token')

    def __str__(self):
        return f"Email: {self.user} ||| Token: {self.token}"