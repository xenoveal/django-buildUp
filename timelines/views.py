from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import *
from .others import *
from user.models import UserExtend

allowed_Category = ['Competition', 'Scholarship', 'Seminar', 'Event']
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
        'extended': UserExtend.objects.get(user=requests.user),
        'desc': True,
    }
    if(sort_type == "desc"):
        context["posts"] = context["posts"].order_by('-timestamp')
    else:
        context["posts"] = context["posts"].order_by('timestamp')
        context["desc"] = False
    for i in context["posts"]:
        i.extend = UserExtend.objects.get(user=i.username)
        dt = i.timestamp
        day, hour, mins, sec = get_time(dt)
        i.diff = select_time_to_show(day, hour, mins, sec)
        i.comments = i.get_comment()
        for j in i.comments:
            j.extend = UserExtend.objects.get(user=j.username)
            dt = j.timestamp
            day, hour, mins, sec = get_time(dt)
            j.diff = select_time_to_show(day, hour, mins, sec)
    return render(requests, "timelines/index.html", context)

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
            'extended': UserExtend.objects.get(user=requests.user),
        }

        if(sort_type == "desc"):
            context["posts"] = context["posts"].order_by('-timestamp')
        else:
            context["posts"] = context["posts"].order_by('timestamp')
            context["desc"] = False
        for i in context["posts"]:
            i.extend = UserExtend.objects.get(user=i.username)
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
            category = requests.POST["category"].lower()
            try:
                share = requests.POST["share_timeline"]
            except:
                share = False
            new_post = CollaborationPost(username=user, title=title, paragraph=paragraph, members=members, location=location, category=category)
            if(title != None):
                if(paragraph != None):
                    new_post.save()
            
            try:
                content_id = requests.POST["contentid"]
                content = Content.objects.get(pk=content_id)
                content.teams.add(new_post)
                return HttpResponseRedirect(reverse("search-team", args=('competition', content_id)))
            except:
                pass
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
def joincolabs(requests, post_id, back_details=None):
    user = User.objects.get(username=requests.user) 
    pp = CollaborationPost.objects.get(pk=post_id)
    pp.colabs_join.add(user) 
    if(back_details is not None):
        content_id = pp.for_joined.first().id
        category = pp.for_joined.first().category.name
        return HttpResponseRedirect(reverse('search-team', args=(category, content_id)))
    return HttpResponseRedirect(reverse("collaboration"))

@login_required
def canceljoincolabs(requests, post_id, back_details=None):
    user = User.objects.get(username=requests.user) 
    pp = CollaborationPost.objects.get(pk=post_id)
    pp.colabs_join.remove(user) 
    if(back_details is not None):
        content_id = pp.for_joined.first().id
        category = pp.for_joined.first().category.name
        return HttpResponseRedirect(reverse('search-team', args=(category, content_id, )))
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

@login_required
def information(requests, category):
    context = {
        'page': 'information',
        'category': category[0].upper()+category[1:],
        'contents': Category.objects.get(name=category.lower()).have_content.all(),
        'bookmarked': requests.user.info_bookmarked.all(),
        'extended': UserExtend.objects.get(user=requests.user),
    }
    for i in context["contents"]:
        start = i.held_on_start
        end = i.held_on_end
        i.start_day = to_local_time(start)
        i.end_day = to_local_time(end)
    if(context['category'] not in allowed_Category):
        return HttpResponseRedirect(reverse('information', args=['competition']))
    return render(requests, "timelines/information.html", context=context)

@login_required
def information_detail(requests, category, content_id):
    context = {
        'page': 'information',
        'category': category[0].upper()+category[1:],
        'content': Content.objects.get(pk=content_id),
        'bookmarked': requests.user.info_bookmarked.all(),
        'extended': UserExtend.objects.get(user=requests.user),
    }
    if(context['category'] not in allowed_Category):
        return HttpResponseRedirect(reverse('information', args=['competition']))
    return render(requests, "timelines/information-detail.html", context=context)

@login_required
def search_team(requests, category, content_id):
    context = {
        'page': 'information',
        'category': category[0].upper()+category[1:],
        'content': Content.objects.get(pk=content_id),
        'joined': requests.user.joined_colabs.all(),
        'extended': UserExtend.objects.get(user=requests.user),
    }
    if(context['category'] not in allowed_Category):
        return HttpResponseRedirect(reverse('information', args=['competition']))
    return render(requests, "timelines/make-party.html", context=context)

@login_required
def bookmarkInfo(requests, category, content_id, back_details=False):
    user = User.objects.get(username=requests.user) 
    pp = Content.objects.get(pk=content_id)
    pp.bookmarked.add(user) 
    if(not back_details):
        return HttpResponseRedirect(reverse("information", args=[category.lower()]))
    return HttpResponseRedirect(reverse("information-detail", args=[category.lower(), content_id]))
    

@login_required
def unbookmarkInfo(requests, category, content_id, back_details=False):
    user = User.objects.get(username=requests.user) 
    pp = Content.objects.get(pk=content_id)
    pp.bookmarked.remove(user) 
    if(not back_details):
        return HttpResponseRedirect(reverse("information", args=[category.lower()]))
    return HttpResponseRedirect(reverse("information-detail", args=[category.lower(), content_id]))