from django.urls import path
from . import views

urlpatterns = [
    path("" , views.Contract.as_view() , name='contract'),
    path("projector", views.Projector.as_view(), name='projector'),
    path("contract/project/<int:pk>", views.Task.as_view(), name='project'),

    path("heartbeat" , views.HeartBeat.as_view() , name="heart_beat"),
    path("starttask" , views.StartTask.as_view() , name='start_task'),
    path("stoptask", views.StopRecord.as_view(), name='stop_task'),

]

