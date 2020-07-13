from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import *
from .others import get_time, select_time_to_show, checker

# Create your views here.
@login_required
def index(requests, sort_type="desc"):
    liked = requests.user.liked.all()
    comment_liked = requests.user.liked_comment.all()
    bookmarked = requests.user.bookmarked.all()
    context = {
        'page': 'timeline',
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

@login_required
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

@login_required
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

@login_required  
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

@login_required
def join(requests, category_id, content_id):
    user = User.objects.get(username=requests.user) 
    content = Content.objects.get(pk=content_id)
    content.join.add(user)
    return HttpResponseRedirect(reverse("detail", args=(category_id, content_id,)))

@login_required
def left(requests, category_id, content_id):
    user = User.objects.get(username=requests.user) 
    content = Content.objects.get(pk=content_id)
    content.join.remove(user)
    return HttpResponseRedirect(reverse("detail", args=(category_id, content_id,)))

@login_required
def post(requests):
    paragraph = requests.POST["paragraph"]
    privatepost = PrivatePost(username=requests.user, paragraph=paragraph)  
    privatepost.save()
    return HttpResponseRedirect(reverse("index"))

@login_required
def edit(requests, post_id):
    pp = PrivatePost.objects.get(pk=post_id)
    if(requests.POST["username"] == requests.user.username):
        if(requests.POST["paragraph"] != ""):
            pp.paragraph = requests.POST["paragraph"]
            pp.save()
    return HttpResponseRedirect(reverse("index"))

@login_required
def delete(requests, post_id):
    pp = PrivatePost.objects.get(pk=post_id)
    if(requests.POST["username"] == requests.user.username):
        pp.delete() 
    return HttpResponseRedirect(reverse("index"))

@login_required
def like(requests, post_id):
    user = User.objects.get(username=requests.user) 
    pp = PrivatePost.objects.get(pk=post_id)
    pp.liked.add(user) 
    return HttpResponseRedirect(reverse("index"))

@login_required
def unlike(requests, post_id):
    user = User.objects.get(username=requests.user) 
    pp = PrivatePost.objects.get(pk=post_id)
    pp.liked.remove(user) 
    return HttpResponseRedirect(reverse("index"))

@login_required
def bookmark(requests, post_id):
    user = User.objects.get(username=requests.user) 
    pp = PrivatePost.objects.get(pk=post_id)
    pp.bookmarked.add(user) 
    return HttpResponseRedirect(reverse("index"))

@login_required
def unbookmark(requests, post_id):
    user = User.objects.get(username=requests.user) 
    pp = PrivatePost.objects.get(pk=post_id)
    pp.bookmarked.remove(user) 
    return HttpResponseRedirect(reverse("index"))

@login_required
def comment(requests, post_id):
    paragraph = requests.POST["paragraph"]
    privatepost = PrivatePost.objects.get(pk=post_id)
    comment = commentPrivatePost(username=requests.user, post=privatepost, paragraph=paragraph)  
    comment.save()
    return HttpResponseRedirect(reverse("index"))
 
@login_required   
def editcomment(requests, comment_id):
    cpp = commentPrivatePost.objects.get(pk=comment_id)
    if(requests.POST["username"] == requests.user.username):
        if(requests.POST["paragraph"] != ""):
            cpp.paragraph = requests.POST["paragraph"]
            cpp.save()
    return HttpResponseRedirect(reverse("index"))

@login_required    
def deletecomment(requests, comment_id):
    cpp = commentPrivatePost.objects.get(pk=comment_id)
    if(requests.POST["username"] == requests.user.username):
        cpp.delete() 
    return HttpResponseRedirect(reverse("index"))

@login_required
def likecomment(requests, comment_id):
    user = User.objects.get(username=requests.user) 
    cpp = commentPrivatePost.objects.get(pk=comment_id)
    cpp.commentLike.add(user) 
    return HttpResponseRedirect(reverse("index"))

@login_required
def unlikecomment(requests, comment_id):
    user = User.objects.get(username=requests.user) 
    pp = commentPrivatePost.objects.get(pk=comment_id)
    pp.commentLike.remove(user) 
    return HttpResponseRedirect(reverse("index"))

@login_required
def collaboration(requests, sort_type="desc"):
    if(requests.method == 'GET'):
        joined = requests.user.joined_colabs.all()
        bookmark = requests.user.colabs_bookmarked.all()
        context = {
            'posts': CollaborationPost.objects.all(),
            'page': 'collaboration',
            'joined': joined,
            'bookmarked': bookmark,
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
        return render(requests, 'timelines/collaboration.html', context=context)
    elif (requests.method =='POST'):
        try:
            user = User.objects.get(username=requests.user) 
            title = checker(requests.POST["title"]) 
            paragraph = checker(requests.POST["paragraph"])
            members = requests.POST["members"]
            location = requests.POST["location"]
            category = requests.POST["category"]
            try:
                share = requests.POST["share_timeline"]
            except:
                share = False
            new_post = CollaborationPost(username=user, title=title, paragraph=paragraph, members=members, location=location, category=category)
            if(title != None):
                if(paragraph != None):
                    new_post.save()
        except:
            pass
        return HttpResponseRedirect(reverse("collaboration"))

@login_required
def delete_collaboration(requests, post_id):
    cp = CollaborationPost.objects.get(pk=post_id)
    if(requests.POST["username"] == requests.user.username):
        cp.delete() 
    return HttpResponseRedirect(reverse("collaboration"))

@login_required
def edit_collaboration(requests, post_id):
    cp = CollaborationPost.objects.get(pk=post_id)
    if(requests.POST["username"] == requests.user.username):
        try:
            user = User.objects.get(username=requests.user) 
            title = checker(requests.POST["title"]) 
            paragraph = checker(requests.POST["paragraph"])
            members = requests.POST["members"]
            location = requests.POST["location"]
            category = requests.POST["category"]
            if(title != None):
                if(paragraph != None):
                    cp.title = title
                    cp.paragraph = paragraph
                    cp.members = members
                    cp.location = location
                    cp.category = category
                    cp.save()
        except:
            pass
    return HttpResponseRedirect(reverse("collaboration"))

@login_required
def joincolabs(requests, post_id):
    user = User.objects.get(username=requests.user) 
    pp = CollaborationPost.objects.get(pk=post_id)
    pp.colabs_join.add(user) 
    return HttpResponseRedirect(reverse("collaboration"))

@login_required
def canceljoincolabs(requests, post_id):
    user = User.objects.get(username=requests.user) 
    pp = CollaborationPost.objects.get(pk=post_id)
    pp.colabs_join.remove(user) 
    return HttpResponseRedirect(reverse("collaboration"))

@login_required
def bookmarkColabs(requests, post_id):
    user = User.objects.get(username=requests.user) 
    pp = CollaborationPost.objects.get(pk=post_id)
    pp.bookmarked.add(user) 
    return HttpResponseRedirect(reverse("collaboration"))

@login_required
def unbookmarkColabs(requests, post_id):
    user = User.objects.get(username=requests.user) 
    pp = CollaborationPost.objects.get(pk=post_id)
    pp.bookmarked.remove(user) 
    return HttpResponseRedirect(reverse("collaboration"))