from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.main, name="main"),
    path("camera",views.camera, name="camera"), # logitec camera
    #path("table", views.table, name="table"),
    path('main/login/', views.login, name='login'),
    path('main/logout/', views.logout, name='logout'),
]