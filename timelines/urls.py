from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('post', views.post, name="post"),
    path('delete/<int:post_id>', views.delete, name="deletepost"),
    path('like/<int:post_id>', views.like, name="like"),
    path('unlike/<int:post_id>', views.unlike, name="unlike"),
    path('edit/<int:post_id>', views.edit, name="editpost"),


    path('category/<int:category_id>', views.categorypost, name="categorizedpost"),
    path('category/<int:category_id>/add', views.add, name="addtocategory"),
    path('category/<int:category_id>/<int:content_id>', views.detail, name="detail"),
    path('category/<int:category_id>/<int:content_id>/join', views.join, name="join"),
    path('category/<int:category_id>/<int:content_id>/left', views.left, name="left"),
]
