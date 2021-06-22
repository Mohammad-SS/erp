from django.urls import path , include
from . import views
from cartable import urls as cartable_urls
from contracts import urls as contract_urls
urlpatterns = [
    path('' , views.Home.as_view() , name='home'),
    path('dashboard', views.Dashboard.as_view(), name='dashboard'),
    path('logout' , views.Logout.as_view() , name='logout'),
    # Dashboard Sections
    path('dashboard/profile' , views.Dashboard.as_view() , name='profile'),
    path('dashboard/mails' , views.Mails.as_view() , name='mails'),
    path('dashboard/cartable/', include(cartable_urls), name='cartable'),
    path('dashboard/forms', views.Forms.as_view(), name='forms'),
    path('dashboard/belongings', views.Belongings.as_view(), name='belongings'),
    path('dashboard/contract/' , include(contract_urls) , name='contract')

]
