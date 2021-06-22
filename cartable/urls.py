from django.urls import path
from . import views

urlpatterns = [

    # inbox :
    path('inbox', views.Cartable.as_view(), name='cartable_inbox'),
    path('inbox/<int:pk>/read', views.ShowLetter.as_view(), name='cartable_simple_read'),
    path('inbox/<int:pk>/read/newreference', views.NewReference.as_view(), name="cartable_new_reference"),
    path('inbox/<int:pk>/read/deletereference', views.DeleteReference.as_view(), name="cartable_delete_reference"),

    # outbox :
    path('write/<int:pk>/send', views.OnGoingLetter.as_view(), name='cartable_out_letter'),
    path('write/send', views.SendLetter.as_view(), name='cartable_send_letter'),
    path('write', views.Write.as_view(), name='cartable_write'),
    path('write/detail', views.Detail.as_view(), name='cartable_detail'),
    path('write/save', views.SaveLetter.as_view(), name='cartable_save'),
    path('outbox' , views.CartableOut.as_view() , name='cartable_outbox'),

    # drafts :
    path('drafts' , views.CartableDrafts.as_view() , name="cartable_drafts")
]
