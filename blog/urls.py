from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="blog"),
    path('post', views.post, name="blog_post"),
]
