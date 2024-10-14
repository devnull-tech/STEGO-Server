from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_container_list, name='get_container_list'),
    path('<int:container_id>/', views.get_container, name='get_container'),
    path('<int:container_id>/input/', views.inupt, name='inupt'),
    path('generate/', views.generate_container, name='generate')
]