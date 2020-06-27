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
        return render(requests, "user/sign-up.html", {"message": None})
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
            return render(requests, "user/sign-up.html", {"message": "Email already exist"})
        return HttpResponseRedirect("verify/1/"+email)
    return render(requests, "user/sign-up.html", {"message": "Password not match"})

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
                from_email='BuildUp! <verification@buildup-id.xyz>',
                recipient_list=[username],
                fail_silently=False,
            )
            token.save()
        except:
            return HttpResponseServerError("<h1>Failed to Send, please resend the verification code</h1>")
        context = {
            "username": username,
            "method": 2
        }          
        if(method==1):
            return render(requests, "user/verify-signup.html", context)
        elif(method==2):
            return render(requests, "user/verify-resend.html", context)
    return HttpResponseRedirect(reverse("index"))

def verified(requests, token):
    try:
        db_token = Token.objects.get(token=token)
    except:
        raise Http404("Token doesn't Exist")
    verify_user = User.objects.get(have_token=db_token)
    if(confirm_token(token)):
        user =  UserExtend(user=verify_user)
        user.verified = True
        user.save()
        Token.objects.filter(user = verify_user).delete()
        return render(requests, "user/verify-success.html")
    else:
        context = {
            "username": verify_user.username,
            "method": 2
        }
        return render(requests, "user/verify-expired.html", context)

def loginform(requests):
    if not requests.user.is_authenticated:
        return render(requests, "user/sign-in.html", {"message": None})
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
        return render(requests, "user/sign-in.html", {"message": "Invalid Credentials"})

def logout_view(requests):
    logout(requests)
    return render(requests, "user/sign-in.html", {"message": "Logged out."})

def forgot_view(requests):
    if requests.method=='GET':
        if not requests.user.is_authenticated:
            return render(requests, "user/forgot-password.html")
        return HttpResponseRedirect(reverse("index"))
    elif requests.method=='POST':
        username = requests.POST["usernameForgot"]
        return HttpResponseRedirect("forgot/"+username)

def forgotsend(requests, username):
    if not requests.user.is_authenticated:
        t = generate_confirmation_token(username)
        link = hosting_url+'/forgot/change/'+t
        context = {
            "username": username.split('@')[0],
            "link": link
            }        
        msg = render_to_string("user/mail.html", context)
        plain_message = strip_tags(msg)
        try:
            token = Token(token=t, user=User.objects.get(username=username))
            send_mail(
                subject=f"Reset BuildUp! Password {username.split('@')[0]}",
                message=plain_message,
                html_message=msg,
                from_email='BuildUp! <verification@buildup-id.xyz>',
                recipient_list=[username],
                fail_silently=False,
            )
            token.save()
        except:
            return HttpResponseServerError("<h1>Failed to Send, please resend the reset password url </h1>")
        context = {
            "username": username,
        }          
        return render(requests, "user/forgot-sendmail.html", context)
    return HttpResponseRedirect(reverse("index"))

def forgotchange(requests, token):
    if(requests.method=="GET"):
        return render(requests, "user/forgot-change.html", {"token": token})
    elif(requests.method=="POST"):
        password = requests.POST["registerPass"]
        password2 = requests.POST["registerPass2"]
        if(password==password2):
            try:
                db_token = Token.objects.get(token=token)
            except:
                raise Http404("Token doesn't Exist")
            verify_user = User.objects.get(have_token=db_token)
            verify_user.set_password(password)
            verify_user.save()
            Token.objects.filter(user = verify_user).delete()
            return render(requests, "user/forgot-success.html")
        context = {"message": "Password not match", "token": token}
        return render(requests, "user/forgot-change.html", context)