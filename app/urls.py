from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    path('', views.index),
    path('logreg/', views.logReg),
    path('login/', views.login),
    path('reg/', views.reg),
    path('logout/', views.logout),
    path('dashboard/', views.dashboard),
]