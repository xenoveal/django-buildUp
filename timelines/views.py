from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import *
import datetime

# Create your views here.
@login_required
def index(requests):
    try:
        liked = requests.user.liked.all()
    except:
        liked = None
    try:
        bookmarked = requests.user.bookmarked.all()
    except:
        bookmarked = None
    context = {
        'categories': Category.objects.all(),
        'posts': PrivatePost.objects.all(),
        'login': requests.user.is_authenticated,
        'user': requests.user,
        'liked': liked,
        'bookmarked': bookmarked
    }
    now = datetime.datetime.now(datetime.timezone.utc)
    context["posts"] = context["posts"].order_by('-timestamp')
    for i in context["posts"]:
        time = now - i.timestamp
        sec = time.total_seconds()
        day = divmod(sec, 24*60*60)[0]
        hour = divmod(sec, 60*60)[0] - day*24
        mins = divmod(sec, 60)[0] - hour*60
        sec = sec - mins*60
        if(day<1):
            if(hour<1):
                if(mins<1):
                    i.diff = str(int(sec))+' seconds ago'
                else:
                    i.diff = str(int(mins))+' mins ago'
            else:
                i.diff = str(int(hour))+' hour ago'
        else:
            i.diff = str(int(day))+' day ago'
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

def edit(requests, post_id):
    pp = PrivatePost.objects.get(pk=post_id)
    if(requests.POST["username"] == requests.user.username):
        if(requests.POST["paragraph"] != ""):
            pp.paragraph = requests.POST["paragraph"]
            pp.save()
    return HttpResponseRedirect(reverse("index"))

def comment(requests, post_id):
    paragraph = requests.POST["paragraph"]
    privatepost = PrivatePost.objects.get(pk=post_id)
    comment = commentPrivatePost(username=requests.user, post=privatepost, paragraph=paragraph)  
    comment.save()
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
