from django.urls import path
from . import views
urlpatterns = [
    # path('chat/<str:idd>/',views.chat,name='chat'),

    path('viewchat/',views.viewchat,name='viewchat'),

]
