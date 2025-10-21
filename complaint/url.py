from django.urls import path
from . import views
urlpatterns = [
path('postcom/',views.post_comp,name='postcom'),

    path('viewcom/',views.view_comp,name='viewcom'),

    path('postreply/<str:idd>/', views.post_reply, name='postreply'),


    path('viewreply/',views.viewreply,name='viewreply'),
]