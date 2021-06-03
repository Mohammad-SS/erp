from django.urls import path
from . import views
urlpatterns = [
    path('inbox' , views.Cartable.as_view() , name='cartable_inbox'),
    path('write' , views.Write.as_view() , name='cartable_write'),
    path('write/detail', views.Detail.as_view(), name='cartable_detail'),
    path('write/contacts', views.Contact.as_view(), name='cartable_contacts'),

]
