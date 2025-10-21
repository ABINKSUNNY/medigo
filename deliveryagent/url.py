from django.urls import path
from . import views
from delivery.models import Delivery
urlpatterns = [
    path('reg_deliveryagent/', views.reg_deliveryagent, name='reg_deliveryagent'),

    path('viewdeliveryagent/', views.viewdeliveryagent, name='viewdeliveryagent'),

    path('deletedeliveryagent/<str:idd>/', views.delete, name='del'),


    # path('assigndelivery/', views.assigndel, name='assigndelivery'),

    path('assign/', views.assign, name='assign'),


]
