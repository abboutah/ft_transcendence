from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path('profile/<str:username>/', views.view_profile, name='view_profile'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("signup/", views.user_signup, name="signup"),
    path('editprofile/', views.profile, name='editprofile'),
    path('ausers/', views.list_users, name='list_users'),
    path('game/', views.game, name='game'),
    path('redirecturi/', views.redirecturi, name='redirecturi'),
    # path('intralogin', views.intralogin, name='intralogin')
    # path('2FAe/', views.email_verification, name='email_verification')
    # path("apix", views.apix),
    # path("apip", views.apip)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #serve user-uploaded media files during development( when debug=True).