from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.middleware import AuthenticationMiddleware
from . import views
from home.views import Index
from home.views import Login
from home.views import SignUp
from home.views import CheckOut
from home.views import Cart
from home.views import OrderView

urlpatterns = [
    #path('', Index.as_view(), name='homepage'),
    path('', views.home, name='home'),

    path('signup', SignUp.as_view(), name='signup'),
    path('login', Login.as_view(), name='login'),
    path('logout', views.Logout, name='logout'),
    path('cart', AuthenticationMiddleware(Cart.as_view()), name='cart'),
    path('check-out', CheckOut.as_view() , name='checkout'),
    path('orders', AuthenticationMiddleware(OrderView.as_view()), name='orders'),
]