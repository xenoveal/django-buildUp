from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import *
from .others import get_time, select_time_to_show

# Create your views here.
@login_required
def index(requests, sort_type="desc"):
    liked = requests.user.liked.all()
    comment_liked = requests.user.liked_comment.all()
    bookmarked = requests.user.bookmarked.all()
    context = {
        'categories': Category.objects.all(),
        'posts': PrivatePost.objects.all(),
        'login': requests.user.is_authenticated,
        'user': requests.user,
        'liked': liked,
        'comment_liked': comment_liked,
        'bookmarked': bookmarked,
        'desc': True,
    }
    if(sort_type == "desc"):
        context["posts"] = context["posts"].order_by('-timestamp')
    else:
        context["posts"] = context["posts"].order_by('timestamp')
        context["desc"] = False
    for i in context["posts"]:
        dt = i.timestamp
        day, hour, mins, sec = get_time(dt)
        i.diff = select_time_to_show(day, hour, mins, sec)
        i.comments = i.get_comment()
        for j in i.comments:
            dt = j.timestamp
            day, hour, mins, sec = get_time(dt)
            j.diff = select_time_to_show(day, hour, mins, sec)
    return render(requests, "timelines/index.html", context)

def categorypost(requests, category_id):
    try:
        category = Category.objects.get(pk=category_id)
        contents = category.content_inside.all() 
    except Category.DoesNotExist:
        raise Http404("Category doesn't Exist")
    context = {
        'category': category,
        'contents': contents,
        'login': requests.user.is_authenticated,
    }
    return render(requests, "timelines/category-post.html", context)

def add(requests, category_id):
    if requests.method != "POST":
        return HttpResponseNotAllowed(requests, "Method not allowed!")
    title = requests.POST["title"]
    paragraph = requests.POST["paragraph"]
    try:
        category = Category.objects.get(pk=category_id)
    except Category.DoesNotExist:
        raise Http404("Category doesn't Exist")
    if(title != "" and paragraph != ""):
        category = Category.objects.get(id=category_id)
        content = Content(title=title, username=requests.user, paragraph=paragraph, category=category)  
        content.save()
    return HttpResponseRedirect(reverse("categorizedpost", args=(category_id,)))
    
def detail(requests, category_id, content_id):
    try:
        content = Content.objects.get(pk=content_id)
    except Content.DoesNotExist:
        raise Http404("Content doesn't Exist")
    context = {
        'content': content,
        'participants': content.join.all(),
        'category': Category.objects.get(id=category_id),
        'login': requests.user.is_authenticated,
    }
    return render(requests, "timelines/detail.html", context)

def join(requests, category_id, content_id):
    user = User.objects.get(username=requests.user) 
    content = Content.objects.get(pk=content_id)
    content.join.add(user)
    return HttpResponseRedirect(reverse("detail", args=(category_id, content_id,)))

def left(requests, category_id, content_id):
    user = User.objects.get(username=requests.user) 
    content = Content.objects.get(pk=content_id)
    content.join.remove(user)
    return HttpResponseRedirect(reverse("detail", args=(category_id, content_id,)))

def post(requests):
    paragraph = requests.POST["paragraph"]
    privatepost = PrivatePost(username=requests.user, paragraph=paragraph)  
    privatepost.save()
    return HttpResponseRedirect(reverse("index"))

def edit(requests, post_id):
    pp = PrivatePost.objects.get(pk=post_id)
    if(requests.POST["username"] == requests.user.username):
        if(requests.POST["paragraph"] != ""):
            pp.paragraph = requests.POST["paragraph"]
            pp.save()
    return HttpResponseRedirect(reverse("index"))

def delete(requests, post_id):
    pp = PrivatePost.objects.get(pk=post_id)
    if(requests.POST["username"] == requests.user.username):
        pp.delete() 
    return HttpResponseRedirect(reverse("index"))

def like(requests, post_id):
    user = User.objects.get(username=requests.user) 
    pp = PrivatePost.objects.get(pk=post_id)
    pp.liked.add(user) 
    return HttpResponseRedirect(reverse("index"))

def unlike(requests, post_id):
    user = User.objects.get(username=requests.user) 
    pp = PrivatePost.objects.get(pk=post_id)
    pp.liked.remove(user) 
    return HttpResponseRedirect(reverse("index"))

def bookmark(requests, post_id):
    user = User.objects.get(username=requests.user) 
    pp = PrivatePost.objects.get(pk=post_id)
    pp.bookmarked.add(user) 
    return HttpResponseRedirect(reverse("index"))

def unbookmark(requests, post_id):
    user = User.objects.get(username=requests.user) 
    pp = PrivatePost.objects.get(pk=post_id)
    pp.bookmarked.remove(user) 
    return HttpResponseRedirect(reverse("index"))

def comment(requests, post_id):
    paragraph = requests.POST["paragraph"]
    privatepost = PrivatePost.objects.get(pk=post_id)
    comment = commentPrivatePost(username=requests.user, post=privatepost, paragraph=paragraph)  
    comment.save()
    return HttpResponseRedirect(reverse("index"))
    
def editcomment(requests, comment_id):
    cpp = commentPrivatePost.objects.get(pk=comment_id)
    if(requests.POST["username"] == requests.user.username):
        if(requests.POST["paragraph"] != ""):
            cpp.paragraph = requests.POST["paragraph"]
            cpp.save()
    return HttpResponseRedirect(reverse("index"))
    
def deletecomment(requests, comment_id):
    cpp = commentPrivatePost.objects.get(pk=comment_id)
    if(requests.POST["username"] == requests.user.username):
        cpp.delete() 
    return HttpResponseRedirect(reverse("index"))

def likecomment(requests, comment_id):
    user = User.objects.get(username=requests.user) 
    cpp = commentPrivatePost.objects.get(pk=comment_id)
    cpp.commentLike.add(user) 
    return HttpResponseRedirect(reverse("index"))

def unlikecomment(requests, comment_id):
    user = User.objects.get(username=requests.user) 
    pp = commentPrivatePost.objects.get(pk=comment_id)
    pp.commentLike.remove(user) 
    return HttpResponseRedirect(reverse("index"))
