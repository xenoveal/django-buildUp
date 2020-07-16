from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('<sort_type>', views.index, name="index"),
    path('post/new', views.post, name="post"),
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

    path('collaboration/all', views.collaboration, name="collaboration"),
    path('collaboration/all/<sort_type>', views.collaboration, name="collaboration"),
    path('collaboration/delete/<int:post_id>', views.delete_collaboration, name="deletecollaboration"),
    path('collaboration/edit/<int:post_id>', views.edit_collaboration, name="editcollaboration"),
    path('collaboration/join/<int:post_id>', views.joincolabs, name="join_colabs"),
    path('collaboration/canceljoin/<int:post_id>', views.canceljoincolabs, name="canceljoin_colabs"),
    path('collaboration/bookmarkcolabs/<int:post_id>', views.bookmarkColabs, name="bookmark_colabs"),
    path('collaboration/unbookmarkcolabs/<int:post_id>', views.unbookmarkColabs, name="unbookmark_colabs"),

    path('information/<str:category>', views.information, name="information"),
    path('information/<str:category>/detail/<int:content_id>', views.information_detail, name="information-detail"),
    path('information/<str:category>/searchteam/<int:content_id>', views.search_team, name="search-team"),
    path('information/<str:category>/bookmarkinfo/<int:content_id>', views.bookmarkInfo, name="bookmark_info"),
    path('information/<str:category>/unbookmarkinfo/<int:content_id>', views.unbookmarkInfo, name="unbookmark_info"),
    path('information/<str:category>/bookmarkinfo/<int:content_id>/<back_details>', views.bookmarkInfo, name="bookmark_info"),
    path('information/<str:category>/unbookmarkinfo/<int:content_id>/<back_details>', views.unbookmarkInfo, name="unbookmark_info"),
    path('information/join/<int:post_id>/<back_details>', views.joincolabs, name="join_colabs"),
    path('information/canceljoin/<int:post_id>/<back_details>', views.canceljoincolabs, name="canceljoin_colabs"),
]
