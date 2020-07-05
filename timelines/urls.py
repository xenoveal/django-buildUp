from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('<sort_type>', views.index, name="index"),
    path('post', views.post, name="post"),
    path('delete/<int:post_id>', views.delete, name="deletepost"),
    path('edit/<int:post_id>', views.edit, name="editpost"),
    path('like/<int:post_id>', views.like, name="like"),
    path('unlike/<int:post_id>', views.unlike, name="unlike"),
    path('bookmark/<int:post_id>', views.bookmark, name="bookmark"),
    path('unbook/<int:post_id>', views.unbookmark, name="unbookmark"),

    path('comment/<int:post_id>', views.comment, name="comment"),
    path('comment/like/<int:comment_id>', views.likecomment, name="like_comment"),
    path('comment/unlike/<int:comment_id>', views.unlikecomment, name="unlike_comment"),
    path('comment/delete/<int:comment_id>', views.deletecomment, name="deletecomment"),
    path('comment/edit/<int:comment_id>', views.editcomment, name="editcomment"),


    path('category/<int:category_id>', views.categorypost, name="categorizedpost"),
    path('category/<int:category_id>/add', views.add, name="addtocategory"),
    path('category/<int:category_id>/<int:content_id>', views.detail, name="detail"),
    path('category/<int:category_id>/<int:content_id>/join', views.join, name="join"),
    path('category/<int:category_id>/<int:content_id>/left', views.left, name="left"),
]
