from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError, Http404
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.urls import reverse
from django.core.mail import send_mail
from .token import *
from .models import *
from time import sleep

hosting_url = 'http://127.0.0.1:8000'

# Create your views here.
def user(requests):
    context = {
        "user": requests.user,
        "login": requests.user.is_authenticated,
    }
    return render(requests, "user/index.html", context)

def registerform(requests):
    if not requests.user.is_authenticated:
        return render(requests, "user/register.html", {"message": None})
    return HttpResponseRedirect(reverse("index"))

def register(requests):
    email = requests.POST["email"].lower()
    first_name = email.split('@')[0]
    first_name = first_name[0].upper() + first_name[1:]
    password = requests.POST["passwordregister"]
    password2 = requests.POST["repeatpassword"]
    if(password==password2):
        try:
            user = User.objects.create_user(username=email, email=email, password=password, first_name=first_name)
            user.save()
            extend = UserExtend(user=user)
            extend.save()
        except:
            return render(requests, "user/register.html", {"message": "Username already exist"})
        return HttpResponseRedirect("verify/1/"+email)
    return render(requests, "user/register.html", {"message": "Password not match"})

def verify(requests, method, username):
    if not requests.user.is_authenticated:
        t = generate_confirmation_token(username)
        link = hosting_url+'/verified/'+t
        context = {
            "username": username.split('@')[0],
            "link": link
            }        
        msg = render_to_string("user/mail.html", context)
        plain_message = strip_tags(msg)
        try:
            token = Token(token=t, user=User.objects.get(username=username))
            send_mail(
                subject=f"Verify Your Account {username.split('@')[0]}",
                message=plain_message,
                html_message=msg,
                from_email='From <verification@buildup-id.xyz>',
                recipient_list=[username],
                fail_silently=False,
            )
            token.save()
        except:
            return HttpResponseServerError("<h1>Failed to Send, please resend the verification code</h1>")             
        if(method==1):
            return render(requests, "user/verification.html", {"message": "Sign Up Successful"})
        elif(method==2):
            return render(requests, "user/verification.html", {"message": "Your Account is not Verified"})
    return HttpResponseRedirect(reverse("index"))

def verified(requests, token):
    try:
        db_token = Token.objects.get(token=token)
    except:
        raise Http404("Token doesn't Exist")
    if(confirm_token(token)):
        verify_user = User.objects.get(have_token=db_token)
        user =  UserExtend(user=verify_user)
        user.verified = True
        user.save()
        Token.objects.filter(user = verify_user).delete()
        return render(requests, "user/verify-success.html")
    else:
        return HttpResponse("Token Expired!")

def loginform(requests):
    if not requests.user.is_authenticated:
        return render(requests, "user/login.html", {"message": None})
    return HttpResponseRedirect(reverse("index"))

def login_me(requests):
    username = requests.POST["username"]
    password = requests.POST["password"]
    user = authenticate(requests, username=username, password=password)
    if user is not None:
        if(UserExtend.objects.get(user=user).verified):
            login(requests, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponseRedirect("verify/2/"+username)
    else:
        return render(requests, "user/login.html", {"message": "Invalid Credentials"})

def logout_view(requests):
    logout(requests)
    return render(requests, "user/login.html", {"message": "Logged out."})