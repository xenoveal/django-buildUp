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

hosting_url = 'https://buildup-id.com'

# Create your views here.

def google_endpoint(request):
    email = request.user.email
    user = User.objects.filter(email=email).first()
    try:
        registered = UserExtend.objects.get(user=user)
        verified = registered.verified
        if(verified):
            return HttpResponseRedirect(reverse("index"))
        else:
            logout(request)
            return HttpResponseRedirect("/verify/2/"+email)
    except: #not registered
        logout(request)
        return render(request, "user/sign-up-google.html", {'email': email})

def google_register(request):
    if(request.method=="POST"):
        email = request.POST["email"]
        password = request.POST["passwordregister"]
        password2 = request.POST["repeatpassword"]
        if(password == password2):
            user = User.objects.filter(email=email).first()
            user.username = email
            user.set_password(password)
            user.save()
            register_user = UserExtend(user=user)
            register_user.save()
            return HttpResponseRedirect("verify/1/"+email)
        else:
            return render(request, "user/sign-up-google.html", {"message": "Password not match", "email": email})

def user(request):
    context = {
        "user": request.user,
        "login": request.user.is_authenticated,
    }
    return render(request, "user/index.html", context)

def registerform(request):
    if not request.user.is_authenticated:
        return render(request, "user/sign-up.html", {"message": None})
    return HttpResponseRedirect(reverse("index"))

def register(request):
    email = request.POST["email"].lower()
    first_name = email.split('@')[0]
    first_name = first_name[0].upper() + first_name[1:]
    password = request.POST["passwordregister"]
    password2 = request.POST["repeatpassword"]
    if(password==password2):
        try:
            user = User.objects.create_user(username=email, email=email, password=password, first_name=first_name)
            user.save()
            extend = UserExtend(user=user)
            extend.save()
        except:
            return render(request, "user/sign-up.html", {"message": "Email already exist"})
        return HttpResponseRedirect("verify/1/"+email)
    return render(request, "user/sign-up.html", {"message": "Password not match"})

def verify(request, method, username):
    if not request.user.is_authenticated:
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
                from_email='BuildUp! <verification@buildup-id.com>',
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
            return render(request, "user/verify-signup.html", context)
        elif(method==2):
            return render(request, "user/verify-resend.html", context)
    return HttpResponseRedirect(reverse("index"))

def verified(request, token):
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
        return render(request, "user/verify-success.html")
    else:
        context = {
            "username": verify_user.username,
            "method": 2
        }
        return render(request, "user/verify-expired.html", context)

def loginform(request):
    if not request.user.is_authenticated:
        return render(request, "user/sign-in.html", {"message": None})
    return HttpResponseRedirect(reverse("index"))

def login_me(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        if(UserExtend.objects.get(user=user).verified):
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponseRedirect("verify/2/"+username)
    else:
        return render(request, "user/sign-in.html", {"message": "Invalid Credentials"})

def logout_view(request):
    logout(request)
    return render(request, "user/sign-in.html", {"message": "Logged out."})

def forgot_view(request):
    if request.method=='GET':
        if not request.user.is_authenticated:
            return render(request, "user/forgot-password.html")
        return HttpResponseRedirect(reverse("index"))
    elif request.method=='POST':
        username = request.POST["usernameForgot"]
        return HttpResponseRedirect("forgot/"+username)

def forgotsend(request, username):
    if not request.user.is_authenticated:
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
        return render(request, "user/forgot-sendmail.html", context)
    return HttpResponseRedirect(reverse("index"))

def forgotchange(request, token):
    if(request.method=="GET"):
        return render(request, "user/forgot-change.html", {"token": token})
    elif(request.method=="POST"):
        password = request.POST["registerPass"]
        password2 = request.POST["registerPass2"]
        if(password==password2):
            try:
                db_token = Token.objects.get(token=token)
            except:
                raise Http404("Token doesn't Exist")
            verify_user = User.objects.get(have_token=db_token)
            verify_user.set_password(password)
            verify_user.save()
            Token.objects.filter(user = verify_user).delete()
            return render(request, "user/forgot-success.html")
        context = {"message": "Password not match", "token": token}
        return render(request, "user/forgot-change.html", context)