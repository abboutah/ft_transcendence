from django.urls import path
from users.views import user_login, user_logout, user_signup, index, callback, intralogin

urlpatterns = [
    path('home/', index, name='home'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('signup/', user_signup, name='signup'),
    path('callback/', callback, name='callback'),
    path('intralogin/', intralogin, name='intralogin'),

]