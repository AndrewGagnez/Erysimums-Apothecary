from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views


from django.contrib.auth.middleware import AuthenticationMiddleware
from home.views import Login
from home.views import SignUp



urlpatterns = [
    path('', views.home, name='home'),
    path('signup', SignUp.as_view(), name='signup'),
    path('login', Login.as_view(), name='login'),
    path('logout', views.Logout, name='logout'),
]