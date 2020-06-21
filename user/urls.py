from django.urls import path

from . import views

urlpatterns = [
    path('', views.user, name="user"),
    path('register', views.registerform, name="registerform"),
    path('registerme', views.register, name="register"),
    path('verify/<int:method>/<str:username>', views.verify, name="verify"),
    path('verified/<str:token>', views.verified, name="verified"),
    path('login', views.loginform, name="loginform"),
    path('loginme', views.login_me, name="login"),
    path('logout', views.logout_view, name="logout")
]