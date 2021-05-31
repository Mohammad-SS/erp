from django.urls import path , include
from . import views
urlpatterns = [
    path('' , views.Home.as_view() , name='home'),
    path('dashboard', views.Dashboard.as_view(), name='dashboard'),
    path('logout' , views.Logout.as_view() , name='logout'),
    path('dashboard/profile' , views.Dashboard.as_view() , name='profile')
]
