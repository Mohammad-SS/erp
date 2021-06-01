from django.urls import path
from . import views
urlpatterns = [
    path('' , views.Cartable.as_view() , name='cartable'),

]
