from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.user, name="user"),
    path('register', views.registerform, name="registerform"),
    path('registerme', views.register, name="register"),
    path('verify/<int:method>/<str:username>', views.verify, name="verify"),
    path('verified/<str:token>', views.verified, name="verified"),
    path('login', views.loginform, name="loginform"),
    path('loginme', views.login_me, name="login"),
    path('logout', views.logout_view, name="logout"),
    path('forgot', views.forgot_view, name= "forgot-password"),
    path('forgot/<str:username>', views.forgotsend, name= "forgotsend"),
    path('forgot/change/<str:token>', views.forgotchange, name= "forgotchange"),
    path('auth/google', views.google_endpoint, name='auth-google'),
    path('google-login', include('social_django.urls', namespace='social')),
    path('google-signup', views.google_register, name='google-signup'),
]