from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseNotAllowed
from django.urls import reverse

# Create your views here.
def index(requests):
    context = {
        'login': requests.user.is_authenticated
    }
    return render(requests, "blog/blog.html", context=context)

def post(requests):
    context = {
        'login': requests.user.is_authenticated
    }
    return render(requests, "blog/blog-open.html", context=context)