from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_detail, name='user_detail'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('update/', views.update_user, name='update_user')
]
