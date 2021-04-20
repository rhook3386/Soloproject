from django.urls import path
from . import views

urlpatterns = [
    path ('', views.home),
    path ('reglog', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('dashboard', views.dashboard),
    path('process_group', views.post_group),
    path('join/<int:id>', views.join),
    path('delete/<int:id>', views.delete),
    path('leave/<int:id>', views.leave),
    path('group/<int:id>', views.group),
]