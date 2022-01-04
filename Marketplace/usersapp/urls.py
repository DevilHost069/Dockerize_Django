from django.urls import path
from . import views

urlpatterns = [
    path('userprofile/', views.userprofile, name="userprofile"),
    path('usersregister/', views.usersregister, name='usersregister'),
    path('userlogin/', views.userlogin, name="userlogin"),
    path('userlogout/', views.userlogout, name="userlogout"),
    path('editprofile/', views.editprofile, name="editprofile"),
    path('usersHome/',views.usersHome,name="usersHome"),
    path('usersAds/',views.usersAds,name="usersAds"),
    path('buyersmessage/',views.buyersMessage,name="buyersmessage"),
    
]